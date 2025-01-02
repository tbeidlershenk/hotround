class Consts:
    dgscene_base_url = 'https://discgolfscene.com'
    dgscene_courses_url = 'https://discgolfscene.com/courses'
    dgscene_state_xpath = '''
        //div[contains(@class, "statelist")]
        //div
        //*
    '''
    dgscene_course_link_xpath = '''
        //div[contains(@id, "courses-big-listing")]
        //a[contains(@href, "/courses/") and @title]
    '''
    dgscene_course_name_header_xpath = '//h1[contains(@class, "header-location")]'

    dgscene_course_events_url = dgscene_base_url + '/courses/{course_name}/events'
    pdga_event_page_base_url = 'https://www.pdga.com/tour/event/'

    dgscene_sanctioned_event_xpath = '''
        //a[span[
            contains(@class, 'info') and 
            contains(@class, 'ts') and (
                contains(text(), 'A-tier') or
                contains(text(), 'B-tier') or
                contains(text(), 'C-tier') or
                contains(text(), 'Major') or
                contains(text(), 'Disc Golf Pro Tour'))]]
    '''
    dgscene_pdga_event_page_xpath = f'//a[contains(@href, "{pdga_event_page_base_url}")]'
    dgscene_pdga_event_page_date_xpath = '//li[contains(@class, "tournament-date")]'


    month_map = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }

    # URLs
    pdgalive_base_url = 'https://www.pdga.com/apps/tournament/live'
    pdgalive_score_page_url = pdgalive_base_url + '/event?eventId={event_id}'
    pdgalive_score_page_specific_division_and_round_url = pdgalive_base_url + \
        '/event?eventId={event_id}&division={division}&view=Scores&round={round_number}'


    # XPaths
    pdgalive_division_picker_xpath = '//div[contains(@class, "division-picker")]'
    pdgalive_division_xpath = '//div[contains(@class, "division-picker")]//button[not(text()="Leaders")]'
    pdgalive_round_xpath = '//div[contains(@class, "division-picker")]/following-sibling::div[1]//div[contains(text(), "Rd")]'
    pdgalive_round_course_metadata_text_xpath = '//div[contains(@class, "round-course-meta")]//text()'
    pdgalive_layout_hole_headers_xpath = "//div[contains(@class, 'hole-header-wrapper')]"
    pdgalive_layout_distances_xpath = "//div[contains(@class, 'header-row')]//div[contains(@class, 'hole-length')]"
    pdgalive_layout_pars_xpath = "//div[contains(@class, 'header-row')]//div[contains(@class, 'label-2')]"
    
    pdgalive_layout_name_xpath = '//div[i[contains(@class, "pi-course-layout")]]'
    pdgalive_course_name_xpath = '//span[contains(@class, "event-name-main")]'
    pdgalive_layout_total_par_xpath = "//div[contains(@class, 'header-col') and contains(string(),'Tot')]//div[contains(@class, 'label-2')]"
    pdgalive_hole_par_xpath = "//div[contains(@class, )]"
    pdgalive_player_row_xpath = '//div[contains(@class, "table-row-content")]'
    pdgalive_player_score_xpath = ".//div[contains(@class, 'round-score')]"
    pdgalive_player_data_xpath = ".//div[contains(@class, 'cell-wrapper')]"
    pdgalive_player_row_cell_xpath = "//div[contains(@class, 'cell-wrapper')]//div"
    pdgalive_hole_score_xpath = ".//div[contains(@class, 'hs')]"

    # Regexes
    round_regex = r'Round (\d)'