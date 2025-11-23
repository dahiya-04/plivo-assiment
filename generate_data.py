import json
import random
import os

# ---------------------------
#  Shared helpers & pools
# ---------------------------

digit_words = ["zero","one","two","three","four","five","six","seven","eight","nine"]

NAMES = [
    # Original
    "rahul sharma", "anita kumar", "arjun reddy", "sneha iyer",
    "ravi verma", "priya singh", "deepak joshi", "nisha patel",
    "vijay nair", "pooja mehta", "akash gupta", "sonali desai",
    # New Additions
    "vikram malhotra", "anjali shukla", "rohan das", "kavita krishnan",
    "suresh menon", "meera reddy", "karthik raman", "divya chopra",
    "amitabh bhattacharya", "swati mishra", "manish tiwari", "isha kapoor",
    "sanjay bansal", "neha agarwal", "rajesh khanna", "tanvi saxena",
    "vivek oberoi", "radhika apte", "siddharth roy", "pallavi chatterjee",
    "varun dhawan", "kareena saif", "ranbir singh", "alia bhatt",
    "mahendra singh", "virat kohli", "rohit sharma", "hardik pandya",
    "sania mirza", "mary kom", "pv sindhu", "saina nehwal",
    "arundhati roy", "salman rushdie", "jhumpa lahiri", "chetan bhagat",
    "narendra modi", "arvind kejriwal", "mamata banerjee", "rahul gandhi"
]

CITIES = [
    # Metros
    "chennai", "mumbai", "delhi", "bangalore", "hyderabad", "pune", "kolkata", "ahmedabad",
    # Tier 2/3
    "jaipur", "lucknow", "surat", "kanpur", "nagpur", "indore", "thane",
    "bhopal", "visakhapatnam", "patna", "vadodara", "ghaziabad", "ludhiana",
    "agra", "nashik", "ranchi", "faridabad", "meerut", "rajkot",
    "varanasi", "srinagar", "aurangabad", "dhanbad", "amritsar", "navi mumbai",
    "allahabad", "coimbatore", "jabalpur", "gwalior", "vijayawada", "jodhpur"
]

LOCATIONS = [
    # Generic & Specific
    "iit madras campus", "central railway station", "airport road",
    "bus stand", "main market", "city mall", "it park",
    "mg road", "indira nagar", "civil lines", "connaught place",
    "marine drive", "jubilee hills", "electronic city", "hitech city",
    "sarjapur road", "bandra west", "south extension", "salt lake city",
    "brigade road", "anna nagar", "koramangala", "whitefield",
    "secunderabad station", "gateway of india", "red fort", "charminar",
    "victoria memorial", "cubbon park", "marina beach", "sankey tank",
    "lotus temple", "qutub minar", "howrah bridge", "amber fort"
]

EMAIL_DOMAINS = [
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", 
    "icloud.com", "proton.me", "live.com", "msn.com", 
    "yahoo.co.in", "rediffmail.com", "aol.com", "zoho.com",
    "yandex.com", "mail.com", "gmx.com", "inbox.com"
]

FILLERS = [
    "uh", "umm", "like", "okay", "yeah", 
    "you know", "actually", "basically", "i mean", "sort of",
    "right", "well", "so", "literally", "totally", "honestly"
]


def verbalize_number(n_str: str) -> str:
    """Convert a string of digits to spoken words: '987' -> 'nine eight seven'."""
    return " ".join(digit_words[int(d)] for d in n_str)


def add_token_spans(text: str, tokens, label: str):
    """
    Create token-level spans so that each token (e.g., 'six', 'two')
    gets its own (start, end, label) entity.
    """
    entities = []
    search_pos = 0
    for tok in tokens:
        start = text.find(tok, search_pos)
        if start != -1:
            end = start + len(tok)
            entities.append({"start": start, "end": end, "label": label})
            search_pos = end
    return entities


def split_pool(pool, train_ratio=0.8):
    """Split a list into disjoint train/dev pools."""
    pool = list(pool)
    random.shuffle(pool)
    k = int(len(pool) * train_ratio)
    return pool[:k], pool[k:]


# -------------------------------------
# Build disjoint entity value pools
# -------------------------------------

def build_entity_pools():
    random.seed(42)

    # Names
    train_names, dev_names = split_pool(NAMES, 0.75)

    # Cities
    train_cities, dev_cities = split_pool(CITIES, 0.75)

    # Locations
    train_locs, dev_locs = split_pool(LOCATIONS, 0.75)

    # Email domains (not super critical, but we can still split)
    train_domains, dev_domains = split_pool(EMAIL_DOMAINS, 0.7)

    # Phone numbers (as digit strings)
    phone_numbers = ["".join(str(random.randint(0, 9)) for _ in range(10)) for _ in range(2000)]
    train_phones, dev_phones = split_pool(phone_numbers, 0.8)

    # Credit card numbers (16-digit strings)
    card_numbers = ["".join(str(random.randint(0, 9)) for _ in range(16)) for _ in range(2000)]
    train_cards, dev_cards = split_pool(card_numbers, 0.8)

    # Date phrases (spoken)
    base_days = [
        "one","two","three","four","five","six","seven","eight","nine","ten",
        "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen",
        "eighteen","nineteen","twenty","twenty one","twenty two","twenty three",
        "twenty four","twenty five","twenty six","twenty seven","twenty eight",
        "twenty nine","thirty","thirty one"
    ]
    base_months = [
        "january","february","march","april","may","june","july","august",
        "september","october","november","december"
    ]
    base_years_train = ["twenty twenty three", "twenty twenty four"]
    base_years_dev = ["two zero two three", "two zero two four", "two zero two five"]

    # Create explicit date pools
    date_train_pool = []
    for d in base_days[:15]:
        for m in base_months[:6]:
            for y in base_years_train:
                date_train_pool.append(f"{d} {m} {y}")
    random.shuffle(date_train_pool)

    date_dev_pool = []
    for d in base_days[10:]:
        for m in base_months[6:]:
            for y in base_years_dev:
                date_dev_pool.append(f"{d} {m} {y}")
    random.shuffle(date_dev_pool)

    pools = {
        "train_names": train_names,
        "dev_names": dev_names,
        "train_cities": train_cities,
        "dev_cities": dev_cities,
        "train_locs": train_locs,
        "dev_locs": dev_locs,
        "train_domains": train_domains,
        "dev_domains": dev_domains,
        "train_phones": train_phones,
        "dev_phones": dev_phones,
        "train_cards": train_cards,
        "dev_cards": dev_cards,
        "train_dates": date_train_pool,
        "dev_dates": date_dev_pool,
    }
    return pools


# -----------------------------------
#   TRAIN example generator
# -----------------------------------

def make_train_example(idx: int, pools):
    """
    Generates one TRAIN example.
    Uses simpler, cleaner templates and noise.
    """
    entities = []
    t = random.choice(["PHONE", "CREDIT_CARD", "EMAIL", "DATE", "CITY_LOC"])

    # PHONE (train)
    if t == "PHONE":
        digits = random.choice(pools["train_phones"])
        spoken = verbalize_number(digits)
        text = f"my phone number is {spoken}"
        entities = add_token_spans(text, spoken.split(), "PHONE")

    # CREDIT_CARD (train)
    elif t == "CREDIT_CARD":
        digits = random.choice(pools["train_cards"])
        spoken = verbalize_number(digits)
        text = f"my credit card number is {spoken}"
        entities = add_token_spans(text, spoken.split(), "CREDIT_CARD")

    # EMAIL + PERSON_NAME (train)
    elif t == "EMAIL":
        name = random.choice(pools["train_names"])
        local_part = name.replace(" ", "").lower()
        domain = random.choice(pools["train_domains"])
        email = f"{local_part}@{domain}"
        spoken = email.replace("@", " at ").replace(".", " dot ")
        text = f"my name is {name} and my email is {spoken}"

        # PERSON_NAME span
        name_start = text.find(name)
        if name_start != -1:
            entities.append({
                "start": name_start,
                "end": name_start + len(name),
                "label": "PERSON_NAME"
            })

        # EMAIL span
        email_start = text.find(spoken)
        if email_start != -1:
            entities.append({
                "start": email_start,
                "end": email_start + len(spoken),
                "label": "EMAIL"
            })

    # DATE (train)
    elif t == "DATE":
        if not pools["train_dates"]:
            date_phrase = "twenty four january twenty twenty four"
        else:
            date_phrase = random.choice(pools["train_dates"])
        text = f"the appointment is on {date_phrase}"
        entities = add_token_spans(text, date_phrase.split(), "DATE")

    # CITY + LOCATION (train)
    elif t == "CITY_LOC":
        city = random.choice(pools["train_cities"])
        loc = random.choice(pools["train_locs"])
        text = f"i am currently in {city} near {loc}"

        c_start = text.find(city)
        if c_start != -1:
            entities.append({
                "start": c_start,
                "end": c_start + len(city),
                "label": "CITY"
            })
        l_start = text.find(loc)
        if l_start != -1:
            entities.append({
                "start": l_start,
                "end": l_start + len(loc),
                "label": "LOCATION"
            })

    return {
        "id": f"train_{idx:04d}",
        "text": text,
        "entities": entities,
    }


# -----------------------------------
#   DEV example generator
# -----------------------------------

def glitch_email(email: str) -> str:
    """Introduce small noise in dev emails (e.g., 'gmail' -> 'gmaill')."""
    if "gmail" in email and random.random() < 0.3:
        return email.replace("gmail", "gmaill")
    return email


def make_dev_example(idx: int, pools):
    """
    Generates one DEV example.
    Uses different templates and more noise.
    """
    entities = []
    t = random.choice(["PHONE", "CREDIT_CARD", "EMAIL", "DATE", "CITY_LOC"])

    # PHONE (dev) - with fillers, different phrasing, 'oh' for zero
    if t == "PHONE":
        digits = random.choice(pools["dev_phones"])
        words = []
        for d in digits:
            w = digit_words[int(d)]
            if d == "0" and random.random() < 0.5:
                w = "oh"  # homophone for zero
            words.append(w)

        core = " ".join(words)

        # insert fillers randomly
        noisy_tokens = []
        for w in core.split():
            if random.random() < 0.2:
                noisy_tokens.append(random.choice(FILLERS))
            noisy_tokens.append(w)

        template = random.choice([
            "you can reach me on {}",
            "please call me at {}",
            "my contact number is {}",
        ])
        text = template.format(" ".join(noisy_tokens))

        entities = add_token_spans(text, core.split(), "PHONE")

    # CREDIT_CARD (dev) - different wording
    elif t == "CREDIT_CARD":
        digits = random.choice(pools["dev_cards"])
        words = verbalize_number(digits).split()

        template = random.choice([
            "the card i used ends in {}",
            "my card number is {}",
            "for payment i used card {}",
        ])
        text = template.format(" ".join(words))
        entities = add_token_spans(text, words, "CREDIT_CARD")

    # EMAIL + PERSON_NAME (dev) - email glitches, different phrasing
    elif t == "EMAIL":
        name = random.choice(pools["dev_names"]).title()
        local_part = name.replace(" ", "")
        domain = random.choice(pools["dev_domains"])
        email = f"{local_part}@{domain}".lower()
        email = glitch_email(email)
        spoken = email.replace("@", " at ").replace(".", " dot ")

        template = random.choice([
            "uh my email address is {} and i am {}",
            "you can mail me at {} my name is {}",
            "the address email happens to be {} and i am called {}",
        ])
        text = template.format(spoken, name)

        name_start = text.find(name)
        if name_start != -1:
            entities.append({
                "start": name_start,
                "end": name_start + len(name),
                "label": "PERSON_NAME"
            })
        email_start = text.find(spoken)
        if email_start != -1:
            entities.append({
                "start": email_start,
                "end": email_start + len(spoken),
                "label": "EMAIL"
            })

    # DATE (dev) - different date style
    elif t == "DATE":
        if not pools["dev_dates"]:
            date_phrase = "two zero two four"
        else:
            date_phrase = random.choice(pools["dev_dates"])

        template = random.choice([
            "appointment on {}",
            "booking is on {}",
            "meeting scheduled for {}",
        ])
        text = template.format(date_phrase)
        entities = add_token_spans(text, date_phrase.split(), "DATE")

    # CITY + LOCATION (dev) - uppercase city, different wording
    elif t == "CITY_LOC":
        city = random.choice(pools["dev_cities"]).upper()
        loc = random.choice(pools["dev_locs"])
        template = random.choice([
            "i stay in {} close to {}",
            "currently in {} near {}",
            "i live around {} by {}",
        ])
        text = template.format(city, loc)

        c_start = text.find(city)
        if c_start != -1:
            entities.append({
                "start": c_start,
                "end": c_start + len(city),
                "label": "CITY"
            })
        l_start = text.find(loc)
        if l_start != -1:
            entities.append({
                "start": l_start,
                "end": l_start + len(loc),
                "label": "LOCATION"
            })

    return {
        "id": f"dev_{idx:04d}",
        "text": text,
        "entities": entities,
    }


# ---------------------------
#   Write datasets
# ---------------------------

def write_jsonl(path, examples):
    with open(path, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")


def main():
    os.makedirs("data", exist_ok=True)
    pools = build_entity_pools()

    # TRAIN
    random.seed(123)
    train_examples = [make_train_example(i, pools) for i in range(1000)]
    write_jsonl("data/train.jsonl", train_examples)

    # DEV
    random.seed(456)
    dev_examples = [make_dev_example(i, pools) for i in range(200)]
    write_jsonl("data/dev.jsonl", dev_examples)

    print("Generated train.jsonl (1000) and dev.jsonl (200) with disjoint pools & different templates/noise.")


if __name__ == "__main__":
    main()
