from UsersApp.models import Professor,Chief

#Returns the most recent section and year assigned to the section chief."""
def get_sectionchief_section(user):
    professor = user.professor  #get professor

    if not professor:
        return None

    chief_assigned = (Chief.objects.filter(professor=professor).order_by('year').first())

    if chief_assigned:
        return chief_assigned.section, chief_assigned.year #return section,year
    else:
        return None, None