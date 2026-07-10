"""Shared metadata taxonomy for Chat Voyage gallery images."""

from __future__ import annotations

from dataclasses import dataclass


LABELS = {
    "daily": "Daily",
    "character": "Character Day",
    "everyday": "Everyday",
    "creative-culture": "Creative Culture",
    "night-out": "Night Out",
    "social-date": "Social / Date",
    "formal-event": "Formal Event",
    "work": "Work",
    "travel": "Travel",
    "movement": "Movement",
    "leisure": "Leisure",
    "home": "Home",
    "weather-layer": "Weather Layer",
    "city-outdoor": "City Outdoor",
    "market-retail": "Market / Retail",
    "museum-gallery": "Museum / Gallery",
    "dining-bar": "Dining / Bar",
    "music-club": "Music / Club",
    "event-venue": "Event Venue",
    "workplace": "Workplace",
    "transit-hub": "Transit Hub",
    "home-interior": "Home Interior",
    "waterfront-resort": "Waterfront / Resort",
    "studio-sports": "Studio / Sports",
    "city-walk": "City Walk",
    "shopping": "Shopping",
    "viewing-design": "Viewing Design",
    "dining-drinks": "Dining / Drinks",
    "dancing": "Dancing",
    "performance-going": "Performance",
    "attending-event": "Attending Event",
    "working": "Working",
    "moving": "Moving",
    "relaxing": "Relaxing",
    "holiday": "Holiday",
    "sport-practice": "Sport / Practice",
    "weather-walk": "Weather Walk",
    "casual-separates": "Casual Separates",
    "tailoring": "Tailoring",
    "dress": "Dress",
    "skirt-skort": "Skirt / Skort",
    "trousers-shorts": "Trousers / Shorts",
    "outerwear-layer": "Outerwear Layer",
    "swimwear": "Swimwear",
    "activewear": "Activewear",
    "eveningwear": "Eveningwear",
}


@dataclass(frozen=True)
class ImageMetadata:
    occasion: str
    venue: str
    activity: str
    outfit: str


CATEGORY_META = {
    "street": ("everyday", "city-outdoor", "city-walk"),
    "mode": ("creative-culture", "museum-gallery", "viewing-design"),
    "night": ("night-out", "dining-bar", "dining-drinks"),
    "resort": ("leisure", "waterfront-resort", "holiday"),
    "office": ("work", "workplace", "working"),
    "weekend": ("everyday", "city-outdoor", "city-walk"),
    "date": ("social-date", "dining-bar", "dining-drinks"),
    "formal": ("formal-event", "event-venue", "attending-event"),
    "travel": ("travel", "transit-hub", "moving"),
    "active": ("movement", "studio-sports", "sport-practice"),
    "club": ("night-out", "music-club", "dancing"),
    "lounge": ("night-out", "dining-bar", "dining-drinks"),
    "theater": ("creative-culture", "event-venue", "performance-going"),
    "gallery": ("creative-culture", "museum-gallery", "viewing-design"),
    "ceremony": ("formal-event", "event-venue", "attending-event"),
    "home": ("home", "home-interior", "relaxing"),
    "swim": ("movement", "waterfront-resort", "holiday"),
    "outerwear": ("weather-layer", "city-outdoor", "weather-walk"),
    "dance": ("movement", "studio-sports", "dancing"),
    "market": ("everyday", "market-retail", "shopping"),
    "transit": ("travel", "transit-hub", "moving"),
}


OUTFIT_KEYWORDS = [
    ("swimwear", ("swim", "swimsuit", "one-piece suit", "rash jacket")),
    ("outerwear-layer", ("outerwear", "coat", "jacket", "trench", "anorak", "cape", "rain shell")),
    ("tailoring", ("tailoring", "tailored", "blazer", "suit", "waistcoat", "vest")),
    ("dress", ("dress", "gown", "pinafore", "shirt dress")),
    ("skirt-skort", ("skirt", "skort", "mini", "wrap panel")),
    ("trousers-shorts", ("trouser", "pants", "shorts", "half pants", "jumpsuit")),
    ("activewear", ("active", "dance", "rehearsal", "paddleboard", "climbing", "sport")),
    ("eveningwear", ("satin", "velvet", "lace", "cocktail", "formal", "ceremony", "theater")),
]


def classify_image(category: str, *text_parts: str) -> ImageMetadata:
    occasion, venue, activity = CATEGORY_META.get(
        category,
        ("everyday", "city-outdoor", "city-walk"),
    )
    text = " ".join(part.lower() for part in text_parts if part)
    outfit = "casual-separates"
    for slug, keywords in OUTFIT_KEYWORDS:
        if any(keyword in text for keyword in keywords):
            outfit = slug
            break
    return ImageMetadata(occasion=occasion, venue=venue, activity=activity, outfit=outfit)


def labelize_metadata(value: str) -> str:
    if value in LABELS:
        return LABELS[value]
    special = {"3d": "3D", "cg": "CG", "pbr": "PBR", "v2": "V2"}
    return " ".join(special.get(part, part.capitalize()) for part in value.split("-"))
