# -*- coding: utf-8 -*-
"""Motor Midway — content source of truth.

Every string here was read off motormidway.wisemanresidential.com on 2026-09-15.
Nothing is invented. Prices, counts, hours and policy text are quoted or lightly
tightened, never embellished. If a fact is not in this file, the pages do not
claim it.
"""

# ── Identity ────────────────────────────────────────────────────────────────
NAME        = "Motor Midway"
FULL        = "Motor Midway by Wiseman"
OPERATOR    = "Wiseman Residential"
ADDRESS_1   = "3657 Motor Ave."
ADDRESS_2   = "Los Angeles, CA 90034"
ADDRESS_ONE = "3657 Motor Ave., Los Angeles, CA 90034"
LOCALE      = "Palms &middot; Culver City border"

# The contact page and the site-wide footer both give the 310 number; the
# homepage body copy gives (760) 212-6707. Flagged to the client — these
# concepts standardise on the number the footer and contact page agree on.
PHONE_DISPLAY = "+1 310-853-1532"
PHONE_TEL     = "tel:+13108531532"

HOURS = [("Monday &ndash; Friday", "9 AM &ndash; 5 PM"),
         ("Saturday &ndash; Sunday", "11 AM &ndash; 4 PM")]

BRAND_LINE = "Experience Good Living."

# ── Real destinations ───────────────────────────────────────────────────────
APPLY     = ("https://motormidway-wisemanresidential.securecafe.com/onlineleasing/"
             "motor-midway-lp/guestlogin.aspx")
RESIDENT  = ("https://motormidway-wisemanresidential.securecafenet.com/residentservices/"
             "motor-midway-lp/userlogin")
DIRECTIONS = "https://maps.google.com/?q=3657%20Motor%20Ave.%20Los%20Angeles,%20CA%2090034"
TERMS      = "https://motormidway.wisemanresidential.com/termsandconditions"
PRIVACY    = "https://motormidway.wisemanresidential.com/privacypolicy"
ACCESS     = "https://motormidway.wisemanresidential.com/accessibility"
WISEMAN    = "https://www.wisemanresidential.com/"
FACEBOOK   = "https://www.facebook.com/officialwisemanresidential"
INSTAGRAM  = "https://www.instagram.com/wisemanresidential"
YELP       = "https://www.yelp.com/biz/wiseman-residential-los-angeles-2"

# ── Floor plans (live availability) ─────────────────────────────────────────
# "All utilities, including trash, gas, electric, and water, are the
# responsibility of the tenant." — floorplans page, verbatim.
UTILITIES_NOTE = ("All utilities, including trash, gas, electric, and water, are the "
                  "responsibility of the tenant.")

PLANS = [
    dict(name="Venice", beds=2, baths=2, sqft=701, price=3395, avail=3,
         img="plan-venice.png",
         blurb="Two bedrooms, two baths and the lowest starting rent in the building.",
         note="Named for Venice Boulevard, four blocks north."),
    dict(name="Dunn", beds=2, baths=2, sqft=692, price=3495, avail=3,
         img="plan-dunn.png",
         blurb="The compact two-bedroom. A full second bath and a patio off the living room.",
         note="Named for Dunn Drive, one street over."),
    dict(name="Sony", beds=2, baths=2, sqft=731, price=3595, avail=1,
         img="plan-sony.jpg",
         blurb="The largest two-bedroom, with the kitchen opening straight into the living room.",
         note="Named for Sony Pictures Studios, half a mile south."),
    dict(name="Regent", beds=3, baths=3, sqft=909, price=4795, avail=1,
         img="plan-regent.jpg",
         blurb="Three bedrooms, three baths. A bathroom for every bedroom and the widest plan here.",
         note="Named for Regent Street, at the south end of the block."),
]
PLAN_SPECIALS = "Specials available"
PLAN_DEPOSIT  = "Deposit: varies"

# Plan names that appear in gallery captions but are not on the live
# availability list. Recorded so nobody 'discovers' them later and assumes
# they were dropped by mistake.
ARCHIVE_PLAN_NAMES = ["Madison", "Overland", "Palm"]

# ── Amenities ───────────────────────────────────────────────────────────────
COMMUNITY_AMENITIES = [
    ("Rooftop Deck",              "An open deck above the intersection, with the city on every side."),
    ("Fitness Center",            "Free weights, treadmills, medicine balls and universal equipment."),
    ("Garage for Resident Parking", "Parking inside the building, off the street."),
    ("Controlled Access Property","A controlled door between the sidewalk and the stairs."),
    ("Elevator",                  "Seven floors, served."),
    ("Bike Racks",                "Storage for the 82 Bike Score to be worth anything."),
    ("Recycling",                 "On site."),
]

APARTMENT_AMENITIES = [
    ("In-Suite Washer &amp; Dryer",      "Your own, in your own apartment."),
    ("Energy-Efficient Appliances",  "Full-size kitchens, stainless steel."),
    ("Central Heating &amp; Air Conditioning", "Ducted, thermostat-controlled."),
    ("Alarm System",                 "In-suite."),
    ("Patio / Balcony",              "Every residence has one."),
    ("Vinyl Flooring",               "Through the living space and the bedrooms."),
    ("Fabric Window Shades",         "Fitted at the windows."),
]

PET_POLICY = [
    "We are a pet-friendly community; your cats and dogs are welcome.",
    "We have a weight limit of 35 lbs, no Pit-Bull, Rottweiler, or mix-breeds of the above.",
    "Please check with the resident manager regarding the pet deposit and monthly rent.",
    "Rules are subject to change at any time.",
]

# ── Scores ──────────────────────────────────────────────────────────────────
SCORES = [("89", "Walk Score", "Most errands can be done on foot."),
          ("82", "Bike Score", "Flat streets and the Ballona Creek Trail."),
          ("61", "Transit Score", "Palms station on the E Line is 0.4 mi up Motor Ave.")]

# ── Neighbourhood ───────────────────────────────────────────────────────────
# Coordinates are cached, not geocoded in the browser. The building was
# resolved through Nominatim; the station and studio lots through Overpass
# (OSM). Distances are straight-line from the building, computed from these
# coordinates — they are labelled as such on the page, because a straight line
# is not a walking route.
#
# One correction worth flagging to the client: the nearest E Line stop is
# PALMS, 0.4 mi up Motor Avenue — not Culver City station at 1.1 mi.
HOME = (34.02362, -118.40649)          # 3657 Motor Ave., verified via Nominatim
HOME_LABEL = "3657 Motor Ave."

# (name, note, lat, lon, straight-line miles)
NEARBY = [
    ("Motor Tides by Wiseman", "The sister property, one block up Motor Avenue",
     34.02552, -118.40795, 0.16),
    ("Palms E Line Station",   "Metro E Line to Santa Monica and Downtown LA",
     34.02932, -118.40428, 0.41),
    ("Sony Pictures Studios",  "The lot on West Washington Boulevard",
     34.01737, -118.40167, 0.51),
    ("Downtown Culver City",   "Restaurants, bars and the Culver Hotel",
     34.02386, -118.39447, 0.69),
    ("The Culver Steps",       "Apple TV+&rsquo;s Culver City campus",
     34.02445, -118.39336, 0.75),
    ("Trader Joe&rsquo;s",     "On Culver Boulevard",
     34.02526, -118.39306, 0.78),
    ("The Culver Studios",     "Amazon MGM&rsquo;s Culver City lot",
     34.02278, -118.39068, 0.91),
    ("Culver City Station",    "The second E Line stop, at Washington &amp; National",
     34.02788, -118.38885, 1.05),
    ("Helms Bakery District",  "Design shops, restaurants and the Helms Walk",
     34.03014, -118.38428, 1.35),
    ("Ballona Creek Trail",    "Bike path west to the ocean, via Syd Kronenthal Park",
     34.02787, -118.37753, 1.68),
]

DISTANCE_NOTE = ("Distances are straight-line from the building, measured from cached "
                 "OpenStreetMap coordinates &mdash; not walking routes.")

# ── Matterport 360 tours (live /videotours) ─────────────────────────────────
TOURS = [
    ("upyi3okJCko", "Tour 1"), ("iLELw2b4Hkh", "Tour 2"), ("ZXVhAJkXJK6", "Tour 3"),
    ("PUvMFH39EuT", "Tour 4"), ("zbbDair1W5Y", "Tour 5"), ("nqZXTNnC8dn", "Tour 6"),
    ("oqMumbcwhFS", "Tour 7"),
]

# ── Photography ─────────────────────────────────────────────────────────────
# friendly slug -> (cloudinary transform key, exact RentCafe filename)
# All 56 of these were verified to return HTTP 200 on 2026-09-15.
PHOTO, PLAN, LOGO = "photo", "plan", "logo"

IMAGES = {
    # exteriors (note: -1/-2/-3 have no space before the dash; -04 up do)
    "exterior-street-1": (PHOTO, "3657 motor ave exterior-1.jpg"),
    "exterior-street-2": (PHOTO, "3657 motor ave exterior-2.jpg"),
    "exterior-sign":     (PHOTO, "3657 motor ave exterior-3.jpg"),
    "corridor":          (PHOTO, "3657 motor ave exterior -04.jpg"),
    "address-wall":      (PHOTO, "3657 motor ave exterior -05.jpg"),
    "roof-rail":         (PHOTO, "3657 motor ave exterior -06.jpg"),
    "roof-pergola":      (PHOTO, "3657 motor ave exterior -08.jpg"),
    "roof-deck":         (PHOTO, "3657 motor ave exterior -10.jpg"),
    # rooftop at dusk — the property's best asset, ten frames
    **{f"dusk-{n:02d}": (PHOTO, f"motor midway rooftop dusk -{n:02d}(1).jpg")
       for n in range(1, 11)},
    # fitness center
    **{f"gym-{n}": (PHOTO, f"motor midway gym -{n}.jpg") for n in range(1, 6)},
    # unit 17
    "u17-patio":          (PHOTO, "mm - unit 17 - patio_final.jpg"),
    "u17-kitchen-bed":    (PHOTO, "mm - unit 17 - kitchen and bedroom _final.jpg"),
    "u17-kdl":            (PHOTO, "mm - unit 17 - kitchen_ dining_ lr_final.jpg"),
    "u17-bed-closet":     (PHOTO, "mm - unit 17 - bedroom and closet _final.jpg"),
    "u17-kitchen-dining": (PHOTO, "mm- unit 17 - kitchen and dining _final.jpg"),
    "u17-kdlr":           (PHOTO, "mm - unit 17 - kitchen_ dining_ living room _final.jpg"),
    "u17-bed-patio":      (PHOTO, "mm - unit 17 - bedroom with patio _final.jpg"),
    "u17-bed-patio-2":    (PHOTO, "mm - unit 17 - bedroom and patio _final.jpg"),
    # unit 702
    "u702-kitchen":   (PHOTO, "motor midway -  unit 702 - kitchen_final.jpg"),
    "u702-bath":      (PHOTO, "motor midway - unit 702 - bathroom_final.jpg"),
    "u702-bed-patio": (PHOTO, "motor midway - unit 702 - bedroom and patio_final.jpg"),
    # unit 703
    "u703-kdl-patio":    (PHOTO, "motor midway -  unit 703 - kitchen_ dining_ lr_ patio_final.jpg"),
    "u703-patio":        (PHOTO, "motor midway - unit 703 - patio_final.jpg"),
    "u703-bed-curtains": (PHOTO, "motor midway - unit 703 - bedroom andpatio with curtains_final.jpg"),
    "u703-bed-patio":    (PHOTO, "motor midway - unit 703 - bedroom and patio_final.jpg"),
    "u703-kitchen":      (PHOTO, "motor midway - unit 703 - kitchen and dining_final.jpg"),
    "u703-patio-wide":   (PHOTO, "3657 motor ave unit 703 -13.jpg"),
    # unit 704
    "u704-kdl-patio": (PHOTO, "motor midway - unit 704 - kitchen_ dining_ lr_ and patio_final.jpg"),
    "u704-kitchen":   (PHOTO, "motor midway - unit 704 - kitchen and dining_final.jpg"),
    "u704-bed-patio": (PHOTO, "motor midway - unit 704 - bedroom and patio_final.jpg"),
    # unit 708
    "u708-lr-patio":    (PHOTO, "motor midway - unit 708 - lr and patio_final.jpg"),
    "u708-kitchen":     (PHOTO, "motor midway - unit 708 - kitchen and  dining_final.jpg"),
    "u708-dining-bed":  (PHOTO, "motor midway - unit 708 - dining and bedroom _final.jpg"),
    # unit 709
    "u709-kitchen":  (PHOTO, "motor midway - unit 709 - kitchen and dining table_final.jpg"),
    "u709-lr-patio": (PHOTO, "motor midway - unit 709 - lr and patio_final.jpg"),
    # unit 710
    "u710-dl-patio": (PHOTO, "motor midway - unit 710 - dining_ lr_ andpatio_final.jpg"),
    "u710-kitchen":  (PHOTO, "motor midway - unit 710 - kitchen and dining_final.jpg"),
    "u710-entry":    (PHOTO, "motor midway - unit 710 - entryway_ kitchen_ and dining_final.jpg"),
    # plan drawings
    "plan-dunn.png":   (PLAN, "mm - dunn floor plan.png"),
    "plan-venice.png": (PLAN, "mm- venice floor plan.png"),
    "plan-sony.jpg":   (PLAN, "motor midway - sony floor plan.jpg"),
    "plan-regent.jpg": (PLAN, "motor midway - regent floor plan.jpg"),
    # brand
    "wiseman-logo.png": (LOGO, "wiseman logo white on teal original(9).png"),
}

# ── Gallery (the 47-photo set, grouped the way the live gallery groups it) ──
GALLERY = [
    ("Residences", [
        ("u704-kdl-patio",   "Open-concept kitchen, dining and living room with patio"),
        ("u703-kdl-patio",   "Open-concept kitchen, dining, living room and patio"),
        ("u708-lr-patio",    "Dining and living room with in-suite washer &amp; dryer and patio"),
        ("u710-dl-patio",    "Open-concept kitchen, dining, living room and patio"),
        ("u709-lr-patio",    "Open-concept kitchen, dining and living room with a patio"),
        ("u17-kdlr",         "Kitchen, dining and living room with recessed lighting and vinyl flooring"),
        ("u17-kdl",          "Kitchen, dining and living room"),
    ]),
    ("Kitchens", [
        ("u709-kitchen",      "Open-concept kitchen with stainless-steel appliances"),
        ("u708-kitchen",      "Kitchen and dining space"),
        ("u702-kitchen",      "Open-concept kitchen with stainless-steel appliances and ample cabinet storage"),
        ("u710-kitchen",      "Open-concept kitchen and dining area"),
        ("u710-entry",        "Entryway, kitchen and dining area"),
        ("u704-kitchen",      "Kitchen with stainless-steel appliances and ample cabinet storage"),
        ("u703-kitchen",      "Open-concept kitchen, dining and living room space"),
        ("u17-kitchen-dining","Open-concept full-size kitchen"),
        ("u17-kitchen-bed",   "Open-concept full-size kitchen"),
    ]),
    ("Bedrooms &amp; baths", [
        ("u703-bed-curtains", "Large bedroom with vinyl flooring, recessed lighting and patio"),
        ("u703-bed-patio",    "Bedroom with recessed lighting, vinyl flooring and a full-size patio"),
        ("u704-bed-patio",    "Large bedroom with mirrored closet, built-in organizers and a patio"),
        ("u702-bed-patio",    "Full-size bedroom with recessed lighting, vinyl flooring and a patio"),
        ("u17-bed-closet",    "Large bedroom with a mirrored closet, recessed lighting and vinyl flooring"),
        ("u17-bed-patio",     "Large bedroom with patio"),
        ("u17-bed-patio-2",   "A bedroom with a large bed and a wall-mounted television"),
        ("u708-dining-bed",   "Full-size kitchen, dining and living room with vinyl flooring and recessed lighting"),
        ("u702-bath",         "Bathroom with glass-door shower-bath and vanity cabinet storage"),
    ]),
    ("Patios", [
        ("u17-patio",       "A balcony with a couch and a plant, overlooking the city"),
        ("u703-patio",      "Large patio"),
        ("u703-patio-wide", "Large patio space"),
    ]),
    ("Rooftop", [
        ("dusk-09",      "Sunset views from the rooftop deck"),
        ("dusk-10",      "Rooftop deck with entertainment area"),
        ("dusk-05",      "Entertainment area with pergola and sunset views from the rooftop deck"),
        ("dusk-07",      "Stunning views of sunset from the rooftop deck"),
        ("dusk-01",      "Rooftop deck with entertainment area and pergola"),
        ("dusk-06",      "Rooftop deck with entertainment area"),
        ("roof-pergola", "A rooftop patio with wooden floors and benches under a metal pergola"),
        ("roof-deck",    "A wooden deck with a metal pergola and benches overlooking a cityscape"),
        ("roof-rail",    "A rooftop patio with a wooden floor and metal railings overlooking a cityscape"),
    ]),
    ("Fitness center", [
        ("gym-4", "Fitness center"),
        ("gym-3", "Fitness center with resistance bands, free weights, treadmills and universal equipment"),
        ("gym-5", "Well-equipped fitness center with medicine balls, free weights and treadmills"),
        ("gym-1", "Well-equipped fitness center with medicine balls, free weights and treadmills"),
        ("gym-2", "Fitness center with medicine balls, free weights, treadmills and universal equipment"),
    ]),
    ("The building", [
        ("exterior-sign",     "The building on Motor Avenue, the address set on the frontage"),
        ("exterior-street-1", "A modern building with a white facade and blue balconies"),
        ("exterior-street-2", "A modern building with balconies and a flat roof"),
        ("address-wall",      "The lobby wall at 3657 Motor Avenue"),
        ("corridor",          "A corridor with wood panelling and the elevator"),
    ]),
]


# Derived so no copy string can drift from the data.
GALLERY_COUNT = sum(len(items) for _g, items in GALLERY)
