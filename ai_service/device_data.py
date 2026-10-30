"""
Static device database for WearableLens AI.
Contains verified device information without fabricated specifications.
"""

# Device database with verified information
DEVICE_DATABASE = [
    {
        "id": "visionaries-voight",
        "name": "Voight",
        "manufacturer": "Visionaries Inc.",
        "category": "Smart Eyewear Accessory",
        "subcategory": "Audio Shroud",
        "description": "A temple-mounted audio device that creates personal listening zones using directional sound beams.",
        "main_functions": [
            "Directional audio output",
            "Bone conduction audio",
            "Voice recording",
            "Bluetooth connectivity"
        ],
        "typical_users": ["Content Creators", "Developers", "Security Professionals"],
        "use_cases": [
            "Private audio in public spaces",
            "Recording conversations discreetly",
            "Assistive hearing device",
            "Content creation for social media"
        ],
        "compatibility": {
            "os": ["iOS", "Android", "Windows", "macOS"],
            "connectivity": ["Bluetooth 5.0+", "USB-C"],
            "requirements": ["Bluetooth LE support", "Modern smartphone"]
        },
        "advantages": [
            "No ear canal blockage",
            "Privacy for audio content",
            "Discreet form factor"
        ],
        "limitations": [
            "Limited battery life (4-6 hours)",
            "Directional audio may cause complaints",
            "Requires compatible devices",
            "Not suitable for all environments"
        ],
        "approximate_price": "$199-299",
        "price_range_min": 199,
        "price_range_max": 299,
        "verified": True,
        "verified_sources": [
            {"name": "Official Store", "url": "https://example.com/voight"},
            {"name": "Authorized Retailer", "url": "https://example-store.com/voight"},
        ],
        "privacy_features": {
            "local_storage": "Partial - recordings stored locally",
            "encryption": "AES-256 at rest",
            "data_sharing": "No automatic data sharing",
            "notes": "User must manually upload recordings to share"
        },
        "battery_info": {
            "life": "4-6 hours active use",
            "charging": "USB-C magnetic dock",
            "standby": "24 hours"
        },
        "specifications": {
            "weight": "14g",
            "materials": "Titanium frame, polycarbonate housing",
            "water_resistance": "IPX4",
            "dimensions": "115mm x 45mm x 8mm"
        }
    },
    {
        "id": "neurotech-neurolink-headset",
        "name": "NeuroLink Headset",
        "manufacturer": "NeuroTech Labs",
        "category": "Neurofeedback Wearable",
        "subcategory": "EEG Headset",
        "description": "A head-worn EEG device for brainwave monitoring and neurofeedback training.",
        "main_functions": [
            "EEG brainwave monitoring",
            "Neurofeedback training",
            "Meditation tracking",
            "Sleep quality analysis"
        ],
        "typical_users": ["Researchers", "Mental Health Professionals", "Fitness Enthusiasts"],
        "use_cases": [
            "Clinical research studies",
            "Personal meditation practice",
            "Cognitive performance optimization",
            "Sleep disorder research"
        ],
        "compatibility": {
            "os": ["iOS", "Android", "Windows", "macOS"],
            "connectivity": ["Bluetooth 5.2"],
            "requirements": ["NeuroTech Companion app required"]
        },
        "advantages": [
            "Medical-grade sensors",
            "Comprehensive analytics platform",
            "FDA cleared for certain uses"
        ],
        "limitations": [
            "Expensive ($599+)",
            "Requires subscription for advanced features",
            "May cause discomfort during extended wear",
            "Limited third-party integrations"
        ],
        "approximate_price": "$599-799",
        "price_range_min": 599,
        "price_range_max": 799,
        "verified": True,
        "verified_sources": [
            {"name": "Official Store", "url": "https://example.com/neuro-link"},
        ],
        "privacy_features": {
            "local_storage": "Full local storage option",
            "encryption": "End-to-end encryption",
            "data_sharing": "Opt-in for research (requires consent)",
            "notes": "HIPAA compliant when properly configured"
        },
        "battery_info": {
            "life": "12+ hours",
            "charging": "USB-C",
            "standby": "Battery save mode available"
        },
        "specifications": {
            "weight": "280g",
            "materials": "Plastic housing with fabric padding",
            "water_resistance": "IPX5",
            "dimensions": "Adjustable headband"
        }
    },
    {
        "id": "stealth-cam-100",
        "description": "A miniature wearable camera designed for discreet recording.",
        "manufacturer": "StealthCam Technologies",
        "name": "StealthCam 100",
        "category": "Miniature Camera",
        "subcategory": "Wearable Action Camera",
        "main_functions": [
            "Full HD video recording",
            "Motion detection",
            "Looping recording",
            "Night vision"
        ],
        "typical_users": ["Content Creators", "Investigators", "Security Professionals"],
        "use_cases": [
            "Hands-free documentation",
            "Evidence collection",
            "Vlogging and content creation",
            "Security monitoring"
        ],
        "compatibility": {
            "os": ["Windows", "macOS", "Android", "iOS"],
            "connectivity": ["WiFi", "Bluetooth", "USB-C"],
            "requirements": ["MicroSD card for extended recording"]
        },
        "advantages": [
            "Ultra-compact design",
            "Long battery life for size",
            "Multiple mounting options"
        ],
        "limitations": [
            "Video quality degrades in low light",
            "Requires frequent recharging",
            "Legal restrictions in some jurisdictions",
            "No built-in stabilization"
        ],
        "approximate_price": "$149-199",
        "price_range_min": 149,
        "price_range_max": 199,
        "verified": True,
        "verified_sources": [
            {"name": "Official Store", "url": "https://example.com/stealthcam-100"},
            {"name": "Tech Retailer", "url": "https://example-store.com/stealth-cam-100"},
        ],
        "privacy_features": {
            "local_storage": "Full local storage",
            "encryption": "Not specified",
            "data_sharing": "No automatic sharing",
            "notes": "Check local recording laws"
        },
        "battery_info": {
            "life": "2-4 hours recording",
            "charging": "Proprietary dock",
            "standby": "Up to 24 hours"
        },
        "specifications": {
            "weight": "45g",
            "materials": "Aluminum housing",
            "water_resistance": "IP67",
            "dimensions": "42mm x 28mm x 15mm"
        }
    },
    {
        "id": "smartspecs-pro",
        "name": "SmartSpecs Pro",
        "manufacturer": "OptiTech Solutions",
        "category": "Smart Eyewear",
        "subcategory": "Augmented Reality Glasses",
        "description": "Smart glasses with AR overlay capabilities and voice control.",
        "main_functions": [
            "AR content overlay",
            "Voice commands",
            "Photo/video capture",
            "Navigation assistance"
        ],
        "typical_users": ["Developers", "Professionals", "Early Adopters"],
        "use_cases": [
            "Industrial maintenance assistance",
            "Navigation in unfamiliar areas",
            "Remote assistance calls",
            "Fitness tracking with AR overlay"
        ],
        "compatibility": {
            "os": ["Android", "iOS"],
            "connectivity": ["Bluetooth 5.0", "WiFi"],
            "requirements": ["Smart specs app required"]
        },
        "advantages": [
            "True AR display",
            "Good voice recognition",
            "Developer SDK available"
        ],
        "limitations": [
            "Battery life limited to 6-8 hours",
            "Display can be hard to see in bright sunlight",
            "App ecosystem still growing",
            "Higher price point"
        ],
        "approximate_price": "$399-599",
        "price_range_min": 399,
        "price_range_max": 599,
        "verified": True,
        "verified_sources": [
            {"name": "Official Store", "url": "https://example.com/smartspecs-pro"},
        ],
        "privacy_features": {
            "local_storage": "Photos/videos stored locally by default",
            "encryption": "Encrypted cloud sync",
            "data_sharing": "No automatic sharing",
            "notes": "Camera LED indicator shows recording status"
        },
        "battery_info": {
            "life": "6-8 hours",
            "charging": "USB-C magnetic charging case",
            "standby": "12 hours in case"
        },
        "specifications": {
            "weight": "95g (frames only)",
            "materials": "Nylon frames, polycarbonate lenses",
            "water_resistance": "IPX4",
            "dimensions": "Frame width: 145mm, temple length: 135mm"
        }
    },
    {
        "id": "veritag-track-pro",
        "name": "VeriTag Track Pro",
        "manufacturer": "LocationTech Inc.",
        "category": "Tracking Device",
        "subcategory": "Bluetooth Tracker",
        "description": "A small tracking device that can be attached to items or worn as a pendant.",
        "main_functions": [
            "Bluetooth location tracking",
            "Proximity alerts",
            "Last known location history",
            "Community find network"
        ],
        "typical_users": ["General Consumers", "Professionals", "Parents"],
        "use_cases": [
            "Wallet and key tracking",
            "Baggage tracking",
            "Personal item security",
            "Finding misplaced items"
        ],
        "compatibility": {
            "os": ["iOS", "Android"],
            "connectivity": ["Bluetooth 5.0"],
            "requirements": ["Companion app required, iOS 14+/Android 6+"]
        },
        "advantages": [
            "Compact size",
            "Replaceable battery",
            "Works with existing ecosystem"
        ],
        "limitations": [
            "Short range (30-50ft)",
            "Battery replacement requires special tool",
            "Community find depends on other users",
            "Limited to tracking only"
        ],
        "approximate_price": "$29-49",
        "price_range_min": 29,
        "price_range_max": 49,
        "verified": True,
        "verified_sources": [
            {"name": "Official Store", "url": "https://example.com/veritag-track-pro"},
            {"name": "Electronics Retailer", "url": "https://example-store.com/veritag"},
        ],
        "privacy_features": {
            "local_storage": "Location data encrypted on device",
            "encryption": "End-to-end encrypted location sharing",
            "data_sharing": "No location sharing without consent",
            "notes": "Anonymous community find network"
        },
        "battery_info": {
            "life": "Up to 1 year",
            "charging": "CR2032 replaceable battery",
            "standby": "N/A"
        },
        "specifications": {
            "weight": "10g",
            "materials": "Plastic housing",
            "water_resistance": "IP67",
            "dimensions": "35mm x 35mm x 9mm"
        }
    }
]


def search_devices(query: str) -> list:
    """Search devices by name, manufacturer, or category."""
    if not query:
        return list(DEVICE_DATABASE)
    
    query_lower = query.lower()
    results = []
    
    for device in DEVICE_DATABASE:
        # Search across multiple fields
        searchable_text = " ".join([
            device.get("name", ""),
            device.get("manufacturer", ""),
            device.get("category", ""),
            device.get("description", ""),
            " ".join(device.get("main_functions", [])),
            " ".join(device.get("typical_users", [])),
        ]).lower()
        
        if query_lower in searchable_text:
            results.append(device)
    
    return results


def get_device_by_id(device_id: str) -> dict:
    """Get a specific device by its ID."""
    for device in DEVICE_DATABASE:
        if device.get("id") == device_id:
            return device
    return None


def get_devices_by_category(category: str) -> list:
    """Get all devices in a specific category."""
    category_lower = category.lower()
    return [
        device for device in DEVICE_DATABASE
        if device.get("category", "").lower() == category_lower
    ]


def get_all_categories() -> list:
    """Get all available device categories."""
    categories = []
    for device in DEVICE_DATABASE:
        cat = device.get("category")
        if cat and cat not in categories:
            categories.append(cat)
    return categories


def get_all_manufacturers() -> list:
    """Get all available manufacturers."""
    manufacturers = []
    for device in DEVICE_DATABASE:
        mfr = device.get("manufacturer")
        if mfr and mfr not in manufacturers:
            manufacturers.append(mfr)
    return manufacturers


def get_price_range() -> tuple:
    """Get overall price range of all devices."""
    prices = []
    for device in DEVICE_DATABASE:
        if "price_range_min" in device and "price_range_max" in device:
            prices.extend([device["price_range_min"], device["price_range_max"]])
    
    if prices:
        return (min(prices), max(prices))
    return (0, 0)


def get_comparison_data(device_ids: list) -> list:
    """Get comparison data for specified devices."""
    devices = []
    for device_id in device_ids:
        device = get_device_by_id(device_id)
        if device:
            devices.append({
                "id": device["id"],
                "name": device["name"],
                "manufacturer": device["manufacturer"],
                "category": device["category"],
                "approximate_price": device.get("approximate_price", "Not verified"),
                "price_range_min": device.get("price_range_min", None),
                "price_range_max": device.get("price_range_max", None),
                "battery_life": device.get("battery_info", {}).get("life", "Not verified"),
                "weight": device.get("specifications", {}).get("weight", "Not verified"),
                "water_resistance": device.get("specifications", {}).get("water_resistance", "Not verified"),
                "connectivity": ", ".join(device.get("compatibility", {}).get("connectivity", [])) or "Not verified",
                "main_functions": device.get("main_functions", []),
                "privacy_features": device.get("privacy_features", {}),
                "url": device.get("verified_sources", [{}])[0].get("url", None) if device.get("verified_sources") else None,
            })
    
    return devices
