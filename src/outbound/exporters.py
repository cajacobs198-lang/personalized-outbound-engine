import csv
from pathlib import Path


def to_smartlead_csv(emails, path: str | Path):
    """Smartlead expects: email,first_name,subject,body,custom_field_1"""
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["email", "first_name", "subject", "body", "variant"])
        for e in emails:
            w.writerow([e.prospect_email, "", e.subject, e.body, e.variant])


def to_apollo_csv(emails, path: str | Path):
    """Apollo CSV upload: email,subject,body,sequence_step"""
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["email", "subject", "body", "sequence_step"])
        for e in emails:
            w.writerow([e.prospect_email, e.subject, e.body, e.variant])


def to_generic_csv(emails, path: str | Path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["prospect_email", "variant", "subject", "body", "reference", "model"])
        for e in emails:
            w.writerow([e.prospect_email, e.variant, e.subject, e.body, e.reference, e.model])
