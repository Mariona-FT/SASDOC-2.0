from UsersApp.models import Professor,Chief

def get_sectionchief_section(user):
    """Returns the last section assigned to the section chief."""
    professor = user.professor  # Assuming one-to-one relation between user and professor

    if not professor:
        return None

    chief_assignment = (
        Chief.objects.filter(professor=professor)
        .order_by('-year__idYear')  # Order by the latest year
        .first()
    )

    if chief_assignment:
        return chief_assignment.section, chief_assignment.year
    else:
        return None, None