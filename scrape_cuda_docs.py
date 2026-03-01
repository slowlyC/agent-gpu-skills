#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "beautifulsoup4",
#   "html2text",
#   "requests",
# ]
# ///
"""
Unified CUDA documentation scraper.

Scrapes NVIDIA CUDA documentation (PTX ISA, Runtime API, Driver API)
and converts to searchable markdown format.
"""

import argparse
import re
from pathlib import Path
from urllib.parse import urljoin

import html2text
import requests
from bs4 import BeautifulSoup, Tag


class DocumentationScraper:
    """Base class for CUDA documentation scrapers."""

    def __init__(
        self,
        base_url: str,
        output_dir: Path,
        cache_dir: Path | None = None,
        skip_download: bool = False,
        force: bool = False,
    ):
        self.base_url = base_url
        self.output_dir = output_dir
        self.cache_dir = cache_dir or (output_dir.parent / f"{output_dir.name}-raw")
        self.skip_download = skip_download
        self.force = force

        # HTTP session with headers
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
        )

        # html2text configuration
        self.h2t = html2text.HTML2Text()
        self.h2t.body_width = 0
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.ignore_emphasis = False
        self.h2t.skip_internal_links = False
        self.h2t.unicode_snob = True
        self.h2t.decode_errors = "ignore"

    def fetch_page(self, url: str) -> BeautifulSoup | None:
        """Fetch and parse a webpage."""
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def sanitize_filename(self, name: str, section_num: str = "") -> str:
        """Convert title to safe filename."""
        # Remove section number from title if present
        name = re.sub(r"^\d+(\.\d+)*\.?\s*", "", name)
        name = re.sub(r"#.*$", "", name)  # Remove anchors
        name = re.sub(r"\.html?$", "", name)  # Remove extensions
        name = re.sub(r"[^\w\s\-_.]", "", name)  # Remove special chars
        name = re.sub(r"\s+", "-", name)  # Spaces to hyphens
        name = name.lower().strip("-")

        # Add section number prefix if provided
        if section_num:
            name = f"{section_num}-{name}"

        return name if name else "index"

    def extract_main_content(self, soup: BeautifulSoup) -> BeautifulSoup:
        """Extract main documentation content from page."""
        content = soup.find("div", class_="contents")
        if not content:
            content = soup.find("div", id="doc-content") or soup.find("body")
        if not content:
            raise ValueError("Could not find main content")

        # Remove navigation elements
        for nav in content.find_all(
            ["div", "ul"],
            class_=["header", "headertitle", "navigate", "breadcrumb"],
        ):
            nav.decompose()

        for elem in content.find_all(
            ["div"],
            id=["top", "titlearea", "projectlogo", "projectname", "projectbrief"],
        ):
            elem.decompose()

        # Remove large navigation lists
        for textblock in content.find_all("div", class_="textblock"):
            links = textblock.find_all("a", href=True)
            if len(links) > 10:
                html_links = [
                    link for link in links if link.get("href", "").endswith(".html")
                ]
                if len(html_links) > 10:
                    textblock.decompose()

        return content

    def convert_to_markdown(self, soup: BeautifulSoup, page_url: str) -> str:
        """Convert HTML to markdown."""
        content = self.extract_main_content(soup)

        # Make image URLs absolute
        for img in content.find_all("img"):
            src = img.get("src")
            if src and not src.startswith(("http://", "https://")):
                img["src"] = urljoin(page_url, src)

        # Make link URLs absolute
        for link in content.find_all("a"):
            href = link.get("href")
            if href and not href.startswith(("http://", "https://", "#", "mailto:")):
                link["href"] = urljoin(page_url, href)

        markdown = self.h2t.handle(str(content))
        markdown = self._clean_navigation_markdown(markdown)
        markdown = re.sub(r"\n{4,}", "\n\n\n", markdown)
        return markdown.strip()

    def _clean_navigation_markdown(self, markdown: str) -> str:
        """Remove navigation cruft from markdown."""
        lines = markdown.split("\n")
        cleaned_lines = []
        in_nav = False
        found_header = False

        for line in lines:
            if (
                "NVIDIA" in line
                and "Toolkit Documentation" in line
                and not found_header
            ):
                in_nav = True
                continue

            if line.startswith("###") or (
                line.startswith("##") and "Public Members" in line
            ):
                in_nav = False
                found_header = True

            if not in_nav:
                cleaned_lines.append(line)

        return "\n".join(cleaned_lines)


class APIScraper(DocumentationScraper):
    """Scraper for CUDA Runtime and Driver API documentation."""

    def __init__(
        self,
        api_type: str,
        output_dir: Path,
        skip_download: bool = False,
        force: bool = False,
    ):
        base_urls = {
            "runtime": "https://docs.nvidia.com/cuda/cuda-runtime-api/",
            "driver": "https://docs.nvidia.com/cuda/cuda-driver-api/",
        }
        self.api_type = api_type
        super().__init__(
            base_urls[api_type],
            output_dir,
            skip_download=skip_download,
            force=force,
        )

    def discover_pages(self) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
        """Discover module and data structure pages."""
        if self.skip_download:
            modules_dir = self.cache_dir / "modules"
            structures_dir = self.cache_dir / "data-structures"
            modules = (
                [{"filename": f.stem} for f in sorted(modules_dir.glob("*.md"))]
                if modules_dir.exists()
                else []
            )
            structures = (
                [{"filename": f.stem} for f in sorted(structures_dir.glob("*.md"))]
                if structures_dir.exists()
                else []
            )
            return modules, structures

        modules = self._discover_modules()
        structures = self._discover_structures()
        return modules, structures

    def _discover_modules(self) -> list[dict[str, str]]:
        """Discover all module pages."""
        soup = self.fetch_page(urljoin(self.base_url, "modules.html"))
        if not soup:
            return []

        pattern = (
            r"group__CUDA__.*\.html"
            if self.api_type == "driver"
            else r"group__CUDART.*\.html"
        )
        modules = []
        seen = set()

        for link in soup.find_all("a", href=re.compile(pattern)):
            href = link.get("href")
            title = link.get_text(strip=True)
            if href and title and href not in seen:
                seen.add(href)
                modules.append(
                    {
                        "url": urljoin(self.base_url, href),
                        "filename": href,
                        "title": title,
                    }
                )

        print(f"Discovered {len(modules)} module pages")
        return modules

    def _discover_structures(self) -> list[dict[str, str]]:
        """Discover all data structure pages."""
        try:
            soup = self.fetch_page(urljoin(self.base_url, "annotated.html"))
        except Exception as e:
            print(f"Warning: Could not fetch annotated.html: {e}")
            return []

        if not soup:
            return []

        pattern = (
            r"structCU.*\.html"
            if self.api_type == "driver"
            else r"(struct|union).*\.html"
        )
        structures = []
        seen = set()

        for link in soup.find_all("a", href=re.compile(pattern)):
            href = link.get("href")
            title = link.get_text(strip=True)
            if href and title and href not in seen:
                seen.add(href)
                structures.append(
                    {
                        "url": urljoin(self.base_url, href),
                        "filename": href,
                        "title": title,
                    }
                )

        print(f"Discovered {len(structures)} data structure pages")
        return structures

    def scrape_page(self, page_info: dict[str, str], output_path: Path) -> bool:
        """Scrape and save a single page."""
        if output_path.exists() and not self.force:
            print(f"  ✓ Using cached: {output_path.name}")
            return True

        try:
            soup = self.fetch_page(page_info["url"])
            if not soup:
                return False

            markdown = self.convert_to_markdown(soup, page_info["url"])
            header = f"# {page_info['title']}\n\n"
            header += f"**Source:** [{page_info['filename']}]({page_info['url']})\n\n"
            header += "---\n\n"

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(header + markdown, encoding="utf-8")

            print(f"  ✓ Saved: {output_path.name} ({len(header + markdown)} bytes)")
            return True
        except Exception as e:
            print(f"  ✗ Error scraping {page_info['url']}: {e}")
            return False

    def clean_markdown_file(self, file_path: Path) -> tuple[str, int, int]:
        """Clean a markdown file, returning (content, original_size, new_size)."""
        content = file_path.read_text(encoding="utf-8")
        original_size = len(content)

        # Remove duplicate function TOC
        content = self._remove_toc(content)

        # Remove duplicate headers
        content = re.sub(r"(### Functions\s*\n){2,}", "### Functions\n\n", content)

        # Remove footer
        footer_markers = [
            "![](https://docs.nvidia.com/cuda/common/formatting/NVIDIA-LogoBlack.svg)",
            "[Privacy Policy]",
            "Copyright ©",
        ]
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if any(marker in line for marker in footer_markers):
                content = "\n".join(lines[:i])
                break

        # Remove formatting artifacts
        content = content.replace("\n---\n", "\n")
        content = content.replace("\u200b", "")  # Zero-width spaces
        content = re.sub(r" \[inherited\]", "", content)

        # Remove anchor links
        content = re.sub(r"\[([^\]]+)\]\(#[^\)]+\)", r"\1", content)

        # Remove "See also:" sections
        content = self._remove_see_also(content)

        # Remove boilerplate notes
        boilerplate = [
            "Note that this function may also return error codes from previous, asynchronous launches.\n\n",
            "Note that this function may also return error codes from previous, asynchronous launches.",
        ]
        for text in boilerplate:
            content = content.replace(text, "")

        # Remove URLs from links (keep text only)
        content = re.sub(r"\[([^\]]+)\]\(https://[^)]+\)", r"\1", content)
        content = re.sub(r"\[\]\(https://[^)]+\)", "", content)

        # Clean up empty notes and trailing commas
        content = re.sub(r"\nNote:\n\n", "\n", content)
        content = re.sub(r",(\s*)$", r"\1", content, flags=re.MULTILINE)

        # Clean up whitespace
        content = re.sub(r"\n{4,}", "\n\n\n", content)
        content = "\n".join(line.rstrip() for line in content.split("\n"))

        return content, original_size, len(content)

    def _remove_toc(self, content: str) -> str:
        """Remove duplicate function TOC from content."""
        lines = content.split("\n")
        cleaned_lines = []
        in_toc = False
        seen_functions_header = False

        for line in lines:
            # Detect TOC lines (Driver API pattern)
            if (
                ") [" in line
                and "](#" in line
                and any(x in line for x in ["](https://", "CUresult", "CUdeviceptr"])
            ):
                in_toc = True
                continue

            # End of TOC
            if line.strip() == "### Functions":
                if seen_functions_header:
                    in_toc = False
                else:
                    seen_functions_header = True

            if not in_toc:
                cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

    def _remove_see_also(self, content: str) -> str:
        """Remove 'See also:' sections."""
        lines = content.split("\n")
        cleaned_lines = []
        in_see_also = False

        for line in lines:
            if line.strip() == "**See also:**":
                in_see_also = True
                continue

            if in_see_also:
                if (
                    line.startswith("#")
                    or line.startswith("[CUresult]")
                    or line.startswith("[void]")
                ):
                    in_see_also = False
                    cleaned_lines.append(line)
                continue

            cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

    def run(self) -> None:
        """Execute the scraping workflow."""
        print("=" * 70)
        print(f"CUDA {self.api_type.title()} API Documentation Scraper")
        print("=" * 70)

        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if self.skip_download:
            print("\n⚡ SKIP DOWNLOAD MODE - Using cached files")
        else:
            print("\n1. Discovering pages...")

        modules, structures = self.discover_pages()

        if not self.skip_download:
            print(
                f"\nTotal pages: {len(modules) + len(structures)} "
                f"(modules: {len(modules)}, structures: {len(structures)})"
            )

            modules_dir = self.cache_dir / "modules"
            structures_dir = self.cache_dir / "data-structures"
            modules_dir.mkdir(exist_ok=True)
            structures_dir.mkdir(exist_ok=True)

            # Scrape modules
            print("\n2. Scraping module pages...")
            for i, module in enumerate(modules, 1):
                print(f"\n[{i}/{len(modules)}] {module['title']}")
                filename = self.sanitize_filename(module["filename"]) + ".md"
                self.scrape_page(module, modules_dir / filename)

            # Scrape structures
            print("\n3. Scraping data structure pages...")
            for i, struct in enumerate(structures, 1):
                print(f"\n[{i}/{len(structures)}] {struct['title']}")
                filename = self.sanitize_filename(struct["filename"]) + ".md"
                self.scrape_page(struct, structures_dir / filename)

        # Cleanup phase
        print(f"\n{'4' if not self.skip_download else '1'}. Cleaning cached files...")
        cache_modules_dir = self.cache_dir / "modules"
        cache_structures_dir = self.cache_dir / "data-structures"
        out_modules_dir = self.output_dir / "modules"
        out_structures_dir = self.output_dir / "data-structures"
        out_modules_dir.mkdir(exist_ok=True)
        out_structures_dir.mkdir(exist_ok=True)

        total_original = 0
        total_new = 0
        files_cleaned = 0

        for md_file in sorted(cache_modules_dir.glob("*.md")):
            content, orig_size, new_size = self.clean_markdown_file(md_file)
            (out_modules_dir / md_file.name).write_text(content, encoding="utf-8")
            total_original += orig_size
            total_new += new_size
            files_cleaned += 1

        for md_file in sorted(cache_structures_dir.glob("*.md")):
            content, orig_size, new_size = self.clean_markdown_file(md_file)
            (out_structures_dir / md_file.name).write_text(content, encoding="utf-8")
            total_original += orig_size
            total_new += new_size
            files_cleaned += 1

        reduction = (
            (total_original - total_new) / total_original * 100
            if total_original > 0
            else 0
        )
        print(
            f"  Cleaned {files_cleaned} files: "
            f"{total_original:,} → {total_new:,} bytes ({reduction:.1f}% reduction)"
        )

        # Create index
        print(f"\n{'5' if not self.skip_download else '2'}. Creating index...")
        self._create_index(out_modules_dir, out_structures_dir)

        print("\n" + "=" * 70)
        print("COMPLETE")
        print("=" * 70)
        print(f"Output: {self.output_dir} ({total_new/1024/1024:.1f} MB)")

    def _create_index(self, modules_dir: Path, structures_dir: Path) -> None:
        """Create INDEX.md file."""
        modules = sorted(
            [
                {"title": f.stem.replace("-", " ").title(), "filename": f.stem}
                for f in modules_dir.glob("*.md")
            ],
            key=lambda x: x["title"],
        )
        structures = sorted(
            [
                {"title": f.stem.replace("-", " ").title(), "filename": f.stem}
                for f in structures_dir.glob("*.md")
            ],
            key=lambda x: x["title"],
        )

        content = f"# CUDA {self.api_type.title()} API Documentation Index\n\n"
        content += f"**Modules:** {len(modules)}  \n"
        content += f"**Data structures:** {len(structures)}  \n\n"

        content += "## Modules\n\n"
        for module in modules:
            filename = self.sanitize_filename(module["filename"]) + ".md"
            content += f"- [{module['title']}](modules/{filename})\n"

        content += "\n## Data Structures\n\n"
        for struct in structures:
            filename = self.sanitize_filename(struct["filename"]) + ".md"
            content += f"- [{struct['title']}](data-structures/{filename})\n"

        index_path = self.output_dir / "INDEX.md"
        index_path.write_text(content, encoding="utf-8")
        print(f"  ✓ Created: {index_path}")


class PTXScraper(DocumentationScraper):
    """Scraper for PTX ISA single-page documentation."""

    def __init__(self, output_dir: Path):
        super().__init__(
            "https://docs.nvidia.com/cuda/parallel-thread-execution/",
            output_dir,
        )

    def run(self) -> None:
        """Execute PTX scraping workflow."""
        print("=" * 70)
        print("PTX ISA Documentation Scraper")
        print("=" * 70)

        soup = self.fetch_page(f"{self.base_url}index.html")
        if not soup:
            print("Failed to fetch documentation")
            return

        print("\nExtracting sections...")
        sections = self._extract_sections(soup)
        print(f"Found {len(sections)} sections")

        # Organize by chapters
        current_chapter_dir = self.output_dir
        for section in sections:
            if "notice" in section["title"].lower() and section["level"] == 0:
                continue

            if section["level"] == 0:
                chapter_name = self.sanitize_filename(
                    section["title"], section["section_num"]
                )
                current_chapter_dir = self.output_dir / chapter_name
                current_chapter_dir.mkdir(parents=True, exist_ok=True)
                print(f"\nChapter: {section['title']}")

            self._save_section(section, current_chapter_dir)

        print(f"\n✓ Complete! Documentation saved to: {self.output_dir}")

    def _extract_sections(self, soup: BeautifulSoup) -> list[dict]:
        """Extract sections from single-page documentation."""
        content = None
        for selector in [
            {"role": "main"},
            {"class": "document"},
            {"class": "body"},
            {"itemprop": "articleBody"},
        ]:
            content = soup.find("div", selector) or soup.find("section", selector)
            if content:
                break

        if not content:
            return []

        sections = []
        headings = content.find_all(["h1", "h2", "h3", "h4"])

        for heading in headings:
            heading_text = heading.get_text(strip=True)
            if not heading_text:
                continue

            # Extract section number
            section_match = re.match(r"^(\d+(?:\.\d+)*)\.\s*(.+)$", heading_text)
            section_num = section_match.group(1) if section_match else ""
            title = section_match.group(2) if section_match else heading_text

            anchor_id = heading.get("id", "") or (
                heading.find("a").get("id", "") if heading.find("a") else ""
            )
            level = int(heading.name[1]) - 1

            # Collect content
            content_elements = []
            current = heading.next_sibling
            while current:
                if isinstance(current, Tag) and current.name in [
                    "h1",
                    "h2",
                    "h3",
                    "h4",
                ]:
                    current_level = int(current.name[1]) - 1
                    if current_level <= level:
                        break
                if isinstance(current, Tag):
                    content_elements.append(current)
                current = current.next_sibling

            sections.append(
                {
                    "title": title,
                    "section_num": section_num,
                    "level": level,
                    "anchor": anchor_id,
                    "content": content_elements,
                }
            )

        return sections

    def _save_section(self, section: dict, parent_dir: Path) -> None:
        """Save section as markdown file."""
        filename = self.sanitize_filename(section["title"], section["section_num"])
        markdown_parts = []

        # Add heading
        level_prefix = "#" * (section["level"] + 1)
        title_with_num = (
            f"{section['section_num']}. {section['title']}"
            if section["section_num"]
            else section["title"]
        )
        markdown_parts.append(f"{level_prefix} {title_with_num}\n")

        # Add content
        for element in section["content"]:
            for class_name in ["headerlink", "viewcode-link", "navigation", "related"]:
                for unwanted in element.find_all(class_=class_name):
                    unwanted.decompose()

            md = self.h2t.handle(str(element))
            # Fix image URLs
            md = re.sub(
                r"!\[(.*?)\]\(_images/(.*?)\)",
                r"![\1](https://docs.nvidia.com/cuda/parallel-thread-execution/_images/\2)",
                md,
            )
            if md:
                markdown_parts.append(md)

        markdown = "\n\n".join(markdown_parts)
        markdown = re.sub(r"\n{4,}", "\n\n\n", markdown)

        # Write file
        output_file = parent_dir / f"{filename}.md"
        output_file.write_text(markdown, encoding="utf-8")
        print(f"  Saved: {output_file.name}")


class ProgrammingGuideScraper(DocumentationScraper):
    """Scraper for CUDA Programming Guide (multi-page, v13.1+).

    Discovers pages automatically by crawling the part index pages.
    """

    BASE_URL = "https://docs.nvidia.com/cuda/cuda-programming-guide/"
    PART_PAGES = ["part1.html", "part2.html", "part3.html", "part4.html", "part5.html"]

    def __init__(self, output_dir: Path, force: bool = False):
        super().__init__(self.BASE_URL, output_dir, force=force)

    def discover_pages(self) -> dict[str, list[dict[str, str]]]:
        """Discover all chapter pages by crawling part index pages."""
        chapters: dict[str, list[dict[str, str]]] = {}

        for part_page in self.PART_PAGES:
            url = f"{self.BASE_URL}{part_page}"
            soup = self.fetch_page(url)
            if not soup:
                continue

            for link in soup.find_all("a", href=True):
                href = link.get("href", "")
                title = link.get_text(strip=True)
                if not href or not title:
                    continue
                # Match links like "01-introduction/introduction.html"
                if re.match(r"\d{2}-[^/]+/[^/]+\.html$", href):
                    chapter = href.split("/")[0]
                    page_url = urljoin(url, href)
                    if chapter not in chapters:
                        chapters[chapter] = []
                    # Avoid duplicates
                    if not any(p["url"] == page_url for p in chapters[chapter]):
                        chapters[chapter].append({"url": page_url, "title": title})

        return chapters

    def scrape_page(self, url: str, output_path: Path) -> bool:
        """Scrape a single Programming Guide page to markdown."""
        try:
            soup = self.fetch_page(url)
            if not soup:
                return False

            main = (
                soup.find("article")
                or soup.find("div", class_="bd-article-container")
                or soup.find("main")
                or soup.find("body")
            )
            if not main:
                return False

            # Remove nav/UI elements
            for nav in main.find_all(
                ["nav", "div", "a"],
                class_=[
                    "prev-next-area",
                    "bd-sidebar-primary",
                    "bd-sidebar-secondary",
                    "headerlink",
                ],
            ):
                nav.decompose()

            # Remove headerlink anchors (the # symbols)
            for hl in main.find_all("a", class_="headerlink"):
                hl.decompose()

            # Make image URLs absolute
            for img in main.find_all("img"):
                src = img.get("src")
                if src and not src.startswith(("http://", "https://")):
                    img["src"] = urljoin(url, src)

            markdown = self.h2t.handle(str(main))
            markdown = re.sub(r"\n{4,}", "\n\n\n", markdown)
            markdown = markdown.strip()

            header = f"---\nurl: {url}\n---\n\n"
            output_path.write_text(header + markdown, encoding="utf-8")
            return True

        except Exception as e:
            print(f"  ✗ Error: {e}")
            return False

    def run(self) -> None:
        """Execute Programming Guide scraping workflow."""
        print("=" * 70)
        print("CUDA Programming Guide Scraper (v13.1+)")
        print(f"Source: {self.BASE_URL}")
        print("=" * 70)

        self.output_dir.mkdir(parents=True, exist_ok=True)

        print("\n1. Discovering pages from part indices...")
        chapters = self.discover_pages()
        total_pages = sum(len(pages) for pages in chapters.values())
        print(f"   Found {len(chapters)} chapters, {total_pages} pages")

        total_saved = 0
        total_failed = 0
        total_skipped = 0

        print("\n2. Scraping pages...")
        for chapter, pages in sorted(chapters.items()):
            chapter_dir = self.output_dir / chapter
            chapter_dir.mkdir(parents=True, exist_ok=True)
            print(f"\n--- {chapter} ({len(pages)} pages) ---")

            for page_info in pages:
                page_name = page_info["url"].split("/")[-1].replace(".html", "")
                output_path = chapter_dir / f"{page_name}.md"

                if output_path.exists() and not self.force:
                    print(f"  ✓ Cached: {page_name}")
                    total_skipped += 1
                    continue

                if self.scrape_page(page_info["url"], output_path):
                    size = output_path.stat().st_size
                    print(f"  ✓ Saved: {page_name} ({size:,} bytes)")
                    total_saved += 1
                else:
                    print(f"  ✗ Failed: {page_name}")
                    total_failed += 1

        # Create index
        self._create_index(chapters)

        print(f"\nDone: {total_saved} saved, {total_skipped} cached, {total_failed} failed")
        print(f"Output: {self.output_dir}")

    def _create_index(self, chapters: dict[str, list[dict[str, str]]]) -> None:
        """Create INDEX.md for Programming Guide."""
        content = "# CUDA Programming Guide v13.1 Index\n\n"
        for chapter, pages in sorted(chapters.items()):
            chapter_title = chapter.split("-", 1)[1].replace("-", " ").title()
            content += f"\n## {chapter} — {chapter_title}\n\n"
            for page in pages:
                name = page["url"].split("/")[-1].replace(".html", "")
                content += f"- [{page['title']}]({chapter}/{name}.md)\n"

        index_path = self.output_dir / "INDEX.md"
        index_path.write_text(content, encoding="utf-8")
        print(f"  ✓ Created: {index_path}")


PTX_SIMPLE_REPO = "https://raw.githubusercontent.com/facebookexperimental/triton/main/.claude/knowledge"
PTX_SIMPLE_FILES = [
    "ptx-isa-arithmetic.md",
    "ptx-isa-async-copy.md",
    "ptx-isa-barriers.md",
    "ptx-isa-cache-hints.md",
    "ptx-isa-control-flow.md",
    "ptx-isa-data-types.md",
    "ptx-isa-load-store.md",
    "ptx-isa-memory-spaces.md",
    "ptx-isa-misc.md",
    "ptx-isa-sm100-blackwell.md",
    "ptx-isa-sm90-hopper.md",
    "ptx-isa-tensor-cores.md",
    "ptx-isa-warp-ops.md",
]


def update_ptx_simple(output_dir: Path, force: bool = False) -> None:
    """Download condensed PTX ISA files from facebookexperimental/triton."""
    print("=" * 70)
    print("PTX Simple (Condensed) Knowledge Base Updater")
    print(f"Source: {PTX_SIMPLE_REPO}")
    print("=" * 70)

    output_dir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()

    downloaded = 0
    skipped = 0
    failed = 0

    for filename in PTX_SIMPLE_FILES:
        target = output_dir / filename
        if target.exists() and not force:
            print(f"  ✓ Exists: {filename} (use --force to re-download)")
            skipped += 1
            continue

        url = f"{PTX_SIMPLE_REPO}/{filename}"
        try:
            print(f"  Downloading: {filename}")
            resp = session.get(url, timeout=30)
            resp.raise_for_status()
            target.write_text(resp.text, encoding="utf-8")
            print(f"  ✓ Saved: {filename} ({len(resp.text):,} bytes)")
            downloaded += 1
        except Exception as e:
            print(f"  ✗ Failed: {filename}: {e}")
            failed += 1

    print(f"\nDone: {downloaded} downloaded, {skipped} skipped, {failed} failed")
    print(f"Output: {output_dir}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Scrape CUDA documentation to markdown"
    )
    parser.add_argument(
        "api_type",
        choices=["ptx", "runtime", "driver", "ptx-simple", "guide", "all"],
        help="API type to scrape (all = ptx + runtime + driver + ptx-simple + guide)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory (default: cuda_skill/references/<api>-docs)",
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip download, use cached files (runtime/driver only)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if cache exists",
    )

    args = parser.parse_args()

    refs_base = Path("cuda_skill/references")

    if args.api_type == "all":
        # Run all scrapers sequentially
        for api in ["ptx", "runtime", "driver", "ptx-simple", "guide"]:
            print(f"\n{'#' * 70}")
            print(f"# Scraping: {api}")
            print(f"{'#' * 70}\n")
            if api == "ptx-simple":
                update_ptx_simple(refs_base / "ptx-simple", args.force)
            elif api == "guide":
                ProgrammingGuideScraper(
                    refs_base / "cuda-guide", args.force
                ).run()
            elif api == "ptx":
                PTXScraper(refs_base / "ptx-docs").run()
            else:
                APIScraper(
                    api, refs_base / f"cuda-{api}-docs", args.skip_download, args.force
                ).run()
        return

    if args.api_type == "ptx-simple":
        output_dir = args.output_dir or refs_base / "ptx-simple"
        update_ptx_simple(output_dir, args.force)
        return

    if args.api_type == "guide":
        output_dir = args.output_dir or refs_base / "cuda-guide"
        ProgrammingGuideScraper(output_dir, args.force).run()
        return

    # Set default output directory
    if not args.output_dir:
        api_name = "ptx" if args.api_type == "ptx" else f"cuda-{args.api_type}"
        args.output_dir = refs_base / f"{api_name}-docs"

    # Create appropriate scraper
    scraper: PTXScraper | APIScraper
    if args.api_type == "ptx":
        scraper = PTXScraper(args.output_dir)
    else:
        scraper = APIScraper(
            args.api_type, args.output_dir, args.skip_download, args.force
        )

    scraper.run()


if __name__ == "__main__":
    main()
