from django.db import migrations

def seed_grades(apps, schema_editor):
    DimGrade = apps.get_model("mintcastiq", "DimGrade")

    grades = [
        # PSA
        ("PSA", 10.0, "GEM MT", "psa10_overlay"),
        ("PSA", 9.5, "MINT+", "psa9_5_overlay"),
        ("PSA", 9.0, "MINT", "psa9_overlay"),
        ("PSA", 8.5, "NM-MT+", "psa8_5_overlay"),
        ("PSA", 8.0, "NM-MT", "psa8_overlay"),
        ("PSA", 7.5, "NM+", "psa7_5_overlay"),
        ("PSA", 7.0, "NM", "psa7_overlay"),
        ("PSA", 6.5, "EX-MT+", "psa6_5_overlay"),
        ("PSA", 6.0, "EX-MT", "psa6_overlay"),
        ("PSA", 5.5, "EX+", "psa5_5_overlay"),
        ("PSA", 5.0, "EX", "psa5_overlay"),
        ("PSA", 0.0, "AUTHENTIC", "psano_overlay"),
        ("PSA", 0.0, "AUTHENTIC ALTERED", "psaaa_overlay"),

        # BGS
        ("BGS", 10.0, "BLACK LABEL", "bgs10bl_overlay"),
        ("BGS", 10.0, "PRISTINE", "bgs10_overlay"),
        ("BGS", 9.5, "GEM MINT", "bgs9_5_overlay"),
        ("BGS", 9.0, "MINT", "bgs9_overlay"),
        ("BGS", 8.5, "NEAR MINT+", "bgs8_5_overlay"),
        ("BGS", 8.0, "NEAR MINT", "bgs8_overlay"),
        ("BGS", 7.5, "NEAR MINT", "bgs7_5_overlay"),
        ("BGS", 7.0, "NEAR MINT", "bgs7_overlay"),
        ("BGS", 6.5, "EXCELLENT MINT+", "bgs6_5_overlay"),
        ("BGS", 6.0, "EXCELLENT MINT", "bgs6_overlay"),
        ("BGS", 5.5, "EXCELLENT+", "bgs5_5_overlay"),
        ("BGS", 5.0, "EXCELLENT", "bgs5_overlay"),

        # SGC
        ("SGC", 10.0, "GEM MINT", "sgc10_overlay"),
        ("SGC", 9.5, "MINT+", "sgc9_5_overlay"),
        ("SGC", 9.0, "MINT", "sgc9_overlay"),
        ("SGC", 8.5, "NM-MT+", "sgc8_5_overlay"),
        ("SGC", 8.0, "NM-MT", "sgc8_overlay"),
        ("SGC", 7.5, "NM+", "sgc7_5_overlay"),
        ("SGC", 7.0, "NM", "sgc7_overlay"),
        ("SGC", 6.5, "EX-MT+", "sgc6_5_overlay"),
        ("SGC", 6.0, "EX-MT", "sgc6_overlay"),
        ("SGC", 5.5, "EX+", "sgc5_5_overlay"),
        ("SGC", 5.0, "EX", "sgc5_overlay"),

        # CGC
        ("CGC", 10.0, "PRISTINE", "cgc10pr_overlay"),
        ("CGC", 10.0, "GEM MINT", "cgc10_overlay"),
        ("CGC", 9.5, "MINT+", "cgc9_5_overlay"),
        ("CGC", 9.0, "MINT", "cgc9_overlay"),
        ("CGC", 8.5, "NM-MT+", "cgc8_5_overlay"),
        ("CGC", 8.0, "NM-MT", "cgc8_overlay"),
        ("CGC", 7.5, "NM+", "cgc7_5_overlay"),
        ("CGC", 7.0, "NM", "cgc7_overlay"),
        ("CGC", 6.5, "EX-MT+", "cgc6_5_overlay"),
        ("CGC", 6.0, "EX-MT", "cgc6_overlay"),
        ("CGC", 5.5, "EX+", "cgc5_5_overlay"),
        ("CGC", 5.0, "EX", "cgc5_overlay"),

        # Ungraded
        ("UNGRADED", 5.0, "NM-MT+", "raw5_overlay"),
        ("UNGRADED", 4.0, "EX", "raw4_overlay"),
        ("UNGRADED", 3.0, "VG", "raw3_overlay"),
        ("UNGRADED", 2.0, "GOOD", "raw2_overlay"),
        ("UNGRADED", 1.0, "POOR", "raw1_overlay"),
    ]

    DimGrade.objects.bulk_create([
        DimGrade(
            grading_standard=standard,
            numeric_value=value,
            grade_label=label,
            overlay_ref=overlay
        )
        for (standard, value, label, overlay) in grades
    ])


class Migration(migrations.Migration):

    dependencies = [
        ("mintcastiq", "0004_remove_dimgrade_unique_grade_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_grades),
    ]
