from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from store.models import Category, Product
from io import BytesIO


SVG_TEMPLATE = """
<svg xmlns='http://www.w3.org/2000/svg' width='800' height='600'>
  <defs>
    <linearGradient id='g' x1='0' x2='0' y1='0' y2='1'>
      <stop offset='0%' stop-color='{c1}'/>
      <stop offset='100%' stop-color='{c2}'/>
    </linearGradient>
  </defs>
  <rect width='100%' height='100%' fill='url(#g)'/>
  <g fill='rgba(255,255,255,0.9)'>
    <circle cx='120' cy='120' r='90'/>
    <rect x='260' y='240' width='480' height='90' rx='18'/>
  </g>
  <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle'
        font-family='Segoe UI, Roboto, Arial' font-size='42' fill='#0f172a'>{label}</text>
</svg>
"""


DEMO_DATA = {
    "Mobiles": [
        ("Pixel 8 Pro", 86990, "Flagship Android phone with excellent camera."),
        ("iPhone 15", 82990, "Latest iPhone with A17 chip and ProMotion."),
        ("Galaxy S24", 79990, "Premium display and performance with One UI."),
        ("OnePlus 12", 58990, "Fast and smooth experience with OxygenOS."),
    ],
    "Laptops": [
        ("MacBook Air M2", 104990, "Lightweight laptop with Apple Silicon."),
        ("Dell XPS 13", 119990, "Compact ultrabook with InfinityEdge display."),
        ("Lenovo ThinkPad X1", 124990, "Business laptop known for reliability."),
        ("HP Spectre x360", 114990, "Convertible with premium build and OLED option."),
    ],
    "Accessories": [
        ("AirPods Pro", 24990, "Noise-cancelling wireless earbuds."),
        ("Galaxy Watch", 27990, "Smartwatch with fitness tracking."),
        ("Anker Power Bank", 3499, "High-capacity portable charger."),
        ("Logitech MX Master 3", 9495, "Ergonomic wireless mouse."),
    ],
}


PALETTE = [
    ("#60a5fa", "#3b82f6"),  # blue
    ("#f59e0b", "#f97316"),  # amber/orange
    ("#34d399", "#10b981"),  # green
    ("#f472b6", "#ec4899"),  # pink
    ("#a78bfa", "#8b5cf6"),  # violet
]


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-")


def build_svg(label: str, idx: int) -> bytes:
    c1, c2 = PALETTE[idx % len(PALETTE)]
    svg = SVG_TEMPLATE.format(c1=c1, c2=c2, label=label)
    return svg.encode("utf-8")


class Command(BaseCommand):
    help = "Seed demo categories and products with generated SVG images"

    @transaction.atomic
    def handle(self, *args, **options):
        total_products = 0
        for cat_idx, (cat_name, items) in enumerate(DEMO_DATA.items()):
            category, _ = Category.objects.get_or_create(
                name=cat_name, defaults={"slug": slugify(cat_name)}
            )

            for idx, (name, price, desc) in enumerate(items):
                product, created = Product.objects.get_or_create(
                    slug=slugify(name),
                    defaults={
                        "category": category,
                        "name": name,
                        "description": desc,
                        "price": price,
                        "stock": 10,
                        "is_active": True,
                    },
                )
                if created or not product.image:
                    svg_bytes = build_svg(name, idx + cat_idx)
                    product.image.save(
                        f"{product.slug}.svg",
                        ContentFile(svg_bytes),
                        save=True,
                    )
                total_products += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded/updated demo data. Products processed: {total_products}"))


