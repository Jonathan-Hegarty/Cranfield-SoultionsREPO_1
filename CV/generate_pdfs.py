"""One-off script to create placeholder PDFs. Run: python generate_pdfs.py"""
from pathlib import Path


def escape_pdf_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_pdf(title: str, lines: list[str]) -> bytes:
    y = 750
    chunks = [f"BT /F1 18 Tf 72 {y} Td ({escape_pdf_text(title)}) Tj ET"]
    y -= 28
    for line in lines:
        chunks.append(f"BT /F1 12 Tf 72 {y} Td ({escape_pdf_text(line)}) Tj ET")
        y -= 18
    stream = "\n".join(chunks).encode("latin-1", errors="replace")

    objects = [
        b"1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n",
        b"2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj\n",
        b"3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>endobj\n",
        b"4 0 obj<< /Length "
        + str(len(stream)).encode()
        + b" >>stream\n"
        + stream
        + b"\nendstream endobj\n",
        b"5 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\n",
    ]

    header = b"%PDF-1.4\n"
    offsets = [0]
    body_parts = [header]
    for obj in objects:
        offsets.append(sum(len(p) for p in body_parts))
        body_parts.append(obj)
    body = b"".join(body_parts)
    xref_start = len(body)
    xref_lines = ["xref", "0 6", "0000000000 65535 f "]
    for i in range(1, 6):
        xref_lines.append(f"{offsets[i]:010d} 00000 n ")
    trailer = f"trailer<< /Size 6 /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF"
    return body + "\n".join(xref_lines).encode() + b"\n" + trailer.encode()


FILES = {
    "slee-mclemon-cv.pdf": (
        "Slee McLemon - CV (Placeholder)",
        [
            "Co-founder, Cranfield Solutions",
            "Replace this PDF with your real CV.",
        ],
    ),
    "jonathan-hegarty-cv.pdf": (
        "Jonathan Hegarty - CV (Placeholder)",
        [
            "Co-founder, Cranfield Solutions",
            "Replace this PDF with your real CV.",
        ],
    ),
    "slee-mclemon-cert-web.pdf": (
        "Web Development Certificate (Placeholder)",
        ["Slee McLemon", "Example provider, 2025"],
    ),
    "slee-mclemon-cert-cloud.pdf": (
        "Cloud Fundamentals Certificate (Placeholder)",
        ["Slee McLemon", "Example provider, 2024"],
    ),
    "slee-mclemon-cert-leadership.pdf": (
        "Leadership Certificate (Placeholder)",
        ["Slee McLemon", "Example provider, 2023"],
    ),
    "jonathan-hegarty-cert-engineering.pdf": (
        "Software Engineering Certificate (Placeholder)",
        ["Jonathan Hegarty", "Example provider, 2025"],
    ),
    "jonathan-hegarty-cert-database.pdf": (
        "Database Design Certificate (Placeholder)",
        ["Jonathan Hegarty", "Example provider, 2024"],
    ),
    "jonathan-hegarty-cert-security.pdf": (
        "Security Basics Certificate (Placeholder)",
        ["Jonathan Hegarty", "Example provider, 2024"],
    ),
}

if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    for name, (title, lines) in FILES.items():
        (folder / name).write_bytes(build_pdf(title, lines))
    print(f"Wrote {len(FILES)} PDFs to {folder}")
