from UsersApp.models import Professor,Chief

#Returns the most recent section assigned to the section chief."""
def get_sectionchief_section(user):
    professor = user.professor  #get professor

    if not professor:
        return None

    chief_assigned = (Chief.objects.filter(professor=professor).order_by('year').first())

    if chief_assigned:
        return chief_assigned.section
    else:
        return None