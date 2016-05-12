# -*- coding: utf-8 -*-
import requests
import xmltodict

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def format_list(original):
    str_list = ""
    for o in original:
        str_list = '{li},{o}'.format(li=str_list, o=o)
    return str_list


class Eventor:
    EVENTOR_API_URL = 'https://eventor.orientering.se/api/'

    CHAMPIONSHIP = 1
    NATIONAL = 2
    DISTRICT = 3
    CLOSE_RANGE = 4
    CLUB = 5
    INTERNATIONAL = 6

    CLASSIFICATION_ID_MAPPING = {
        1: 'mästerskapstävling',
        2: 'nationell tävling',
        3: 'distriktstävling',
        4: 'närtävling',
        5: 'klubbtävling',
        6: 'internationell tävling'
    }
    EVENT_STATUS_ID_MAPPING = {
        1: 'ansökt',
        2: 'godkänt av distriktet',
        3: 'godkänt',
        4: 'skapat',
        5: 'anmälan öppen',
        6: 'anmälan pausad',
        7: 'anmälan stängd',
        8: 'live',
        9: 'genomförd',
        10: 'inställt',
        11: 'rapporterad'}

    DISCIPLINE_ID_MAPPING = {
        1: 'orienteringlöpning',
        2: 'MTB-orientering',
        3: 'skidorientering',
        4: 'precisionsorientering'}

    EVENT_FORM_MAPPING = {
        'IndSingleDay': 'individuell endagstävling',
        'IndMultiDay': 'individuell flerdagarstävling',
        'RelaySingleDay': 'stafett endagstävling'}

    def __init__(self, api_key):
        self.api_key = api_key

    def _execute(self, function, q):
        url = "{base}{function}".format(base=self.EVENTOR_API_URL, function=function)
        if q:
            query_string = urlencode(q)
            url = "{url}?{query}".format(url=url, query=query_string)

        r = requests.get(url, headers={'ApiKey': self.api_key})
        e = xmltodict.parse(r.text)
        return e

    def events(self,
               from_date='0000-01-01',
               to_date='9999-12-31',
               from_modify_date='0000-01-01 00:00:00',
               to_modify_date='9999-12-31 23:59:59',
               event_ids=None,
               organisation_ids=None,
               classification_ids=None,
               include_entry_breaks=False,
               include_attributes=False):
        """
        GET https://eventor.orientering.se/api/events
        Returnerar en lista med tävlingar som matchar sökparametrarna.

        Query-parametrar
        Namn Obl Standard Beskrivning
        fromDate  0000-01-01 Startdatum (åååå-mm-dd).
        toDate  9999-12-31 Slutdatum (åååå-mm-dd).
        fromModifyDate  0000-01-01 00:00:00 Inkluderar endast tävlingar som ändrats efter denna tidpunkt
            (åååå-mm-dd hh:mm:ss).
        toModifyDate  9999-12-31 23:59:59 Inkluderar endast tävlingar som ändrats före denna tidpunkt
            (åååå-mm-dd hh:mm:ss).
        eventIds   Kommaseparerad lista med tävlings-id:n. Utelämna för att inkludera alla tävlingar.
        organisationIds   Kommaseparerad lista med organisations-id:n för arrangörsklubbarna.
            Om ett distrikts organisations-id anges kommer alla tävlingar som arrangeras av en klubb i distriktet att
            inkluderas. Utelämna för att inkludera alla tävlingar.
        classificationIds   Kommaseparerad lista med tävlingstyps-id:n, där 1=mästerskapstävling, 2=nationell tävling,
            3=distriktstävling, 4=närtävling, 5=klubbtävling, 6=internationell tävling. Utelämna för att inkludera alla
            tävlingar.
        includeEntryBreaks  false Sätt till true för att inkludera tävlingens anmälningsstopp.
        includeAttributes  false Sätt till true för att inkludera tävlingens tävlingsattribut.
        Returnerat element

        EventList
        """
        if include_entry_breaks:
            ieb = 'true'
        else:
            ieb = 'false'

        if include_attributes:
            ia = 'true'
        else:
            ia = 'false'

        q = {'fromDate': from_date,
             'toDate': to_date,
             'fromModifyDate': from_modify_date,
             'toModifyDate': to_modify_date,
             'includeEntryBreaks': ieb,
             'includeAttributes': ia
             }
        if event_ids:
            q['eventIds'] = format_list(event_ids)
        if organisation_ids:
            q['organisationIds'] = format_list(organisation_ids)
        if classification_ids:
            q['classificationIds'] = format_list(classification_ids)

        return self._execute('events', q)

    def events_documents(self,
                         from_date='0000-01-01',
                         to_date='9999-12-31',
                         event_ids=None,
                         organisation_ids=None):
        """
        GET https://eventor.orientering.se/api/events/documents
        Returnerar en lista med dokument för tävlingar som matchar sökparametrarna.

        Query-parametrar
        Namn Obl Standard Beskrivning
        fromDate  0000-01-01 Startdatum (åååå-mm-dd).
        toDate  9999-12-31 Slutdatum (åååå-mm-dd).
        eventIds   Kommaseparerad lista med tävlings-id:n. Utelämna för att inkludera alla tävlingar.
        organisationIds   Kommaseparerad lista med organisations-id:n för arrangörsklubbarna. Om ett distrikts
            organisations-id anges kommer alla tävlingar som arrangeras av en klubb i distriktet att inkluderas.
            Utelämna för att inkludera alla tävlingar.
        Returnerat element

        DocumentList
        """
        q = {'fromDate': from_date,
             'toDate': to_date}
        if event_ids:
            q['eventIds'] = format_list(event_ids)
        if organisation_ids:
            q['organisationIds'] = format_list(organisation_ids)

        return self._execute('events/documents', q)

    def event(self, event_id):
        """
        GET https://eventor.orientering.se/api/event/{eventId}
        Returnerar en tävling.

        Path-parametrar
        Namn Obl Standard Beskrivning
        eventId ja  Tävlingens id enligt /events.
        Returnerat element

        Event
        """
        return self._execute('event/{event_id}'.format(event_id=event_id), None)

    def event_classes(self, event_id, include_entry_fees=False):
        """
        GET https://eventor.orientering.se/api/eventclasses
        Returnerar alla klasser i en tävling.

        Query-parametrar
        Namn Obl Standard Beskrivning
        eventId ja  Tävlingens id enligt /events.
        includeEntryFees   Sätt till true för att inkludera id:n och tillämpningsordning för klassernas
            anmälningsavgifter.
        Returnerat element

        EventClassList
        """
        if include_entry_fees:
            ief = 'true'
        else:
            ief = 'false'

        q = {'eventId': event_id,
             'includeEntryFees': ief}

        return self._execute('eventclasses', q)

    def event_entryfees(self, event_id):
        """
        GET https://eventor.orientering.se/api/entryfees/events/{eventId}
        Returnerar alla anmälningsavgifter i en tävling.

        Path-parametrar
        Namn Obl Standard Beskrivning
        eventId ja  Tävlingens id enligt /events.
        Returnerat element

        EntryFeeList
        """
        return self._execute('entryfees/events/{event_id}'.format(event_id=event_id), None)

    def organisation_from_api_key(self):
        """
        GET https://eventor.orientering.se/api/organisation/apiKey
        Returnerar den organisation som den använda api-nyckeln tillhör.

        Returnerat element

        Organisation
        """
        return self._execute('organisation/apiKey', None)

    def organisations(self, include_properties=False):
        """
        GET https://eventor.orientering.se/api/organisations
        Returnerar en lista med samtliga organisationer (förbund, distriktsförbund och klubbar).

        Query-parametrar
        Namn Obl Standard Beskrivning
        includeProperties  false Sätt till true för att inkludera utökad information om organisationerna.
        Returnerat element

        OrganisationList
        """
        if include_properties:
            ip = 'true'
        else:
            ip = 'false'

        q = {'includeProperties': ip}
        return self._execute('organisations', q)['OrganisationList']['Organisation']

    def organisation(self, organisation_id):
        """
        GET https://eventor.orientering.se/api/organisation/{id}
        Returnerar en organisation (förbund, distriktsförbund och klubbar).

        Path-parametrar
        Namn Obl Standard Beskrivning
        id ja  Organisationens id.
        Returnerat element

        Organisation
        """
        return self._execute('organisation/{organisation_id}'.format(organisation_id=organisation_id), None)

    def members_in_organisation(self, organisation_id, include_contact_details=False):
        """
        GET https://eventor.orientering.se/api/persons/organisations/{organisationId}
        Returnerar alla personer som är medlemmar i en organisation.

        Path-parametrar
        Namn Obl Standard Beskrivning
        organisationId ja  Organisationens id enligt /organisations. Denna parameter måste sättas till den egna
            organisationens id.
        Query-parametrar
        Namn Obl Standard Beskrivning
        includeContactDetails  false Sätt till true för att inkludera medlemmarnas adresser, telefonnummer och
            e-postadresser.
        Returnerat element

        PersonList
        """
        if include_contact_details:
            icd = 'true'
        else:
            icd = 'false'
        q = {'includeContactDetails': icd}
        url = 'persons/organisations/{organisation_id}'.format(organisation_id=organisation_id)
        return self._execute(url, q)['PersonList']['Person']

    def competitors(self, organisation_id):
        """
        GET https://eventor.orientering.se/api/competitors
        Returnerar tävlingsinställningar (bricknummer, förvalda klasser) för alla personer som angett detta i en
            organisation.

        Query-parametrar
        Namn Obl Standard Beskrivning
        organisationId ja  Organisationens id enligt /organisations. Denna parameter måste sättas till den egna
            organisationens id.
        Returnerat element

        CompetitorList
        """
        q = {'organisationId': organisation_id}
        return self._execute('competitors', q)['CompetitorList']['Competitor']

    def external_login_url(self, person_id, organisation_id, include_contact_details=False):
        """
        GET https://eventor.orientering.se/api/externalLoginUrl
        Returnerar en länk som kan användas för att omdirigera en person från en extern sida till inloggat läge i
            Eventor. Länken kan bara användas vid ett tillfälle och förfaller efter fem minuter. Användbar i det fall
            klubben har en hemsidelösning med egen inloggning. Obs! Var noga med att använda denna metod på ett sådant
            sätt så att endast autentiserade användare i det externa systemet har tillgång till omdirigeringslänken!

        Query-parametrar
        Namn Obl Standard Beskrivning
        personId ja  Personens id enligt /persons/organisations/{organisationId}. Personen måste vara medlem i
            organisationen som anges av organisationId.
        organisationId ja  Organisationens id enligt /organisations. Denna parameter måste sättas till den egna
            organisationens id.
        includeContactDetails  false Sätt till true för att inkludera medlemmarnas adresser, telefonnummer och
            e-postadresser.
        Returnerat element

        ExternalLoginUrl
        """
        if include_contact_details:
            icd = 'true'
        else:
            icd = 'false'

        q = {'personId': person_id,
             'organisationId': organisation_id,
             'includeContactDetails': icd}
        return self._execute('externalLoginUrl', q)

    def authenticate_person(self, username, password):
        """
        GET https://eventor.orientering.se/api/authenticatePerson
        Returnerar den person som matchar givet användarnamn och lösenord.

        Header-parametrar
        Namn Obl Standard Beskrivning
        Username ja  Personens användarnamn i Eventor.
        Password ja  Personens lösenord i Eventor.
        Returnerat element

        Person
        """
        q = {'Username': username,
             'Password': password}
        return self._execute('authenticatePerson', q)

    def entries(self,
                organisation_ids=None,
                event_ids=None,
                event_class_ids=None,
                from_event_date='0000-01-01',
                to_event_date='9999-12-31',
                from_entry_date='0000-01-01 00:00:00',
                to_entry_date='9999-12-31 23:59:59',
                from_modify_date='0000-01-01 00:00:00',
                to_modify_date='9999-12-31 23:59:59',
                include_entry_fees=False,
                include_person_element=False,
                include_organisation_element=False,
                include_event_element=False
                ):
        """
        GET https://eventor.orientering.se/api/entries
        Returnerar personer som anmälts till tävlingar enligt sökparametrarna.

        Query-parametrar
        Namn Obl Standard Beskrivning
        organisationIds   Kommaseparerad lista med id:n enligt /organisations för de organisationer som anmälningar
            ska hämtas för. Utelämna för att inkludera alla organisationer.
        eventIds   Kommaseparerad lista med tävlings-id:n enligt /events. Utelämna för att inkludera alla tävlingar.
        eventClassIds   Kommaseparerad lista med klass-id:n enligt /eventclasses. Utelämna för att inkludera alla
            klasser.
        fromEventDate  0000-01-01 Hämtar anmälningar från tävlingar som arrangeras under detta eller senare datum
            (åååå-mm-dd).
        toEventDate  9999-12-31 Hämtar anmälningar från tävlingar som arrangeras under detta eller tidigare datum
            (åååå-mm-dd).
        fromEntryDate  0000-01-01 00:00:00 Hämtar anmälningar som gjorts denna eller senare tidpunkt
            (åååå-mm-dd hh:mm:ss).
        toEntryDate  9999-12-31 23:59:59 Hämtar anmälningar som gjorts denna eller tidigare tidpunkt
            (åååå-mm-dd hh:mm:ss).
        fromModifyDate  0000-01-01 00:00:00 Hämtar anmälningar som ändrats denna eller senare tidpunkt
            (åååå-mm-dd hh:mm:ss).
        toModifyDate  9999-12-31 23:59:59 Hämtar anmälningar som ändrats denna eller tidigare tidpunkt
            (åååå-mm-dd hh:mm:ss).
        includeEntryFees  false Sätt till true för att inkludera information om anmälningsavgifter.
        includePersonElement  false Sätt till true för att inkludera fullständig personinformation i stället för
            enbart person-id.
        includeOrganisationElement  false Sätt till true för att inkludera fullständig organisationsinformation i
            stället för enbart organisations-id.
        includeEventElement  false Sätt till true för att inkludera fullständig tävlingsinformation i stället för
            enbart tävlings-id.
        Returnerat element

        EntryList
        """
        if include_entry_fees:
            ief = 'true'
        else:
            ief = 'false'
        if include_person_element:
            ipe = 'true'
        else:
            ipe = 'false'
        if include_organisation_element:
            ioe = 'true'
        else:
            ioe = 'false'
        if include_event_element:
            iee = 'true'
        else:
            iee = 'false'

        q = {
            'fromEventDate': from_event_date,
            'toEventDate': to_event_date,
            'fromEntryDate': from_entry_date,
            'toEntryDate': to_entry_date,
            'fromModifyDate': from_modify_date,
            'toModifyDate': to_modify_date,
            'includeEntryFees': ief,
            'includePersonElement': ipe,
            'includeOrganisationElement': ioe,
            'includeEventElement': iee,
        }

        if organisation_ids:
            q['organisationIds'] = format_list(organisation_ids)
        if event_ids:
            q['eventIds'] = format_list(event_ids)
        if event_class_ids:
            q['eventClassIds'] = format_list(event_class_ids)
        return self._execute('entries', q)

    def competitor_count(self, organisation_ids, event_ids=None, person_ids=None):
        """
        GET https://eventor.orientering.se/api/competitorcount
        Returnerar antalet tävlingsanmälningar enligt sökparametrarna.

        Query-parametrar
        Namn Obl Standard Beskrivning
        organisationIds ja  Kommaseparerad lista med id:n enligt /organisations för de organisationer som anmälningar
            ska hämtas för.
        eventIds   Kommaseparerad lista med tävlings-id:n enligt /events. Utelämna för att inkludera alla tävlingar.
        personIds   Kommaseparerad lista med person-id:n enligt /persons/organisations/{organisationId}.
            Personerna måste vara medlemmar i organisationen som anges av organisationIds.
        Returnerat element

        CompetitorCountList
        """
        q = {}
        if organisation_ids:
            q['organisationIds'] = format_list(organisation_ids)
        if event_ids:
            q['eventIds'] = format_list(event_ids)
        if person_ids:
            q['personIds'] = format_list(person_ids)
        return self._execute('competitorcount', q)

    def start_times_per_event(self, event_id):
        """
        GET https://eventor.orientering.se/api/starts/event
        Returnerar starttider för en tävling.

        Query-parametrar
        Namn Obl Standard Beskrivning
        eventId   Tävlings-id enligt /events.
        Returnerat element

        StartList
        """
        q = {'eventId': event_id}
        return self._execute('starts/event', q)

    def start_times_per_event_iofxml(self, event_id, event_race_id=None):
        """
        GET https://eventor.orientering.se/api/starts/event/iofxml
        Returnerar starttider i IOF XML 3.0-format för en tävling.

        Query-parametrar
        Namn Obl Standard Beskrivning
        eventId ja  Tävlings-id enligt /events.
        eventRaceId   Etapp-id enligt /events.
        Returnerat element

        IOF XML 3.0 StartList
        """
        q = {'eventId': event_id}
        if event_race_id:
            q['eventRaceId'] = event_race_id
        return self._execute('starts/event/iofxml', q)

    def start_times_per_person(self,
                               person_id,
                               event_ids=None,
                               from_date='0000-01-01',
                               to_date='9999-12-31'):
        """
        GET https://eventor.orientering.se/api/starts/person
        Returnerar starttider för en person på ett antal tävlingar.

        Query-parametrar
        Namn Obl Standard Beskrivning
        personId   Person-id enligt /persons/organisations/{organisationId}.
        eventIds   Kommaseparerad lista med tävlings-id:n enligt /events. Utelämna för att inkludera alla tävlingar.
        fromDate  0000-01-01 Inkluderar tävlingar som arrangeras under detta eller senare datum (åååå-mm-dd).
        toDate  9999-12-31 Inkluderar tävlingar som arrangeras under detta eller tidigare datum (åååå-mm-dd).
        Returnerat element

        StartListList
        """
        q = {'personId': person_id,
             'fromDate': from_date,
             'toDate': to_date}
        if event_ids:
            q['eventIds'] = format_list(event_ids)
        return self._execute('starts/person', q)

    def start_times_per_organisation(self, organisation_ids, event_id=None):
        """
        GET https://eventor.orientering.se/api/starts/organisation
        Returnerar starttider för en organisations (klubbs) deltagare på en tävling.

        Query-parametrar
        Namn Obl Standard Beskrivning
        organisationIds ja  Kommaseparerad lista med id:n enligt /organisations för de organisationer som starttider
            ska hämtas för. Denna parameter måste sättas till den egna organisationens id.
        eventId   Tävlings-id enligt /events.
        Returnerat element

        StartList
        """
        q = {'organisationIds': format_list(organisation_ids)}
        if event_id:
            q['eventId'] = event_id
        return self._execute('starts/organisation', q)

    def results_per_event(self, event_id, include_split_times=False, top=None):
        """
        GET https://eventor.orientering.se/api/results/event
        Returnerar resultat för en tävling.

        Query-parametrar
        Namn Obl Standard Beskrivning
        eventId   Tävlings-id enligt /events.
        includeSplitTimes   Sätt till true för att inkludera sträcktider.
        top   Returnerar endast detta antal deltagare från toppen av resultatlistan. Utelämna för att inkludera alla
            deltagare.
        Returnerat element

        ResultList
        """
        if include_split_times:
            ist = 'true'
        else:
            ist = 'false'
        q = {'eventId': event_id,
             'includeSplitTimes': ist}
        if top:
            q['top'] = top

        return self._execute('results/event', q)

    def results_per_event_iofxml(self,
                                 event_id,
                                 event_race_id=None,
                                 include_split_times=False,
                                 total_result=False):
        """
        GET https://eventor.orientering.se/api/results/event/iofxml
        Returnerar resultat i IOF XML 3.0-format för en tävling.

        Query-parametrar
        Namn Obl Standard Beskrivning
        eventId ja  Tävlings-id enligt /events.
        eventRaceId   Etapp-id enligt /events.
        includeSplitTimes   Sätt till true för att inkludera sträcktider.
        totalResult   Sätt till true för att returnera totalresultat om tävlingen är en fleretappstävling.
        Returnerat element

        IOF XML 3.0 ResultList
        """
        if include_split_times:
            ist = 'true'
        else:
            ist = 'false'
        if total_result:
            tr = 'true'
        else:
            tr = 'false'
        q = {'eventId': event_id,
             'includeSplitTimes': ist,
             'totalResult': tr}
        if event_race_id:
            q['eventRaceId'] = event_race_id
        return self._execute('results/event/iofxml', q)

    def results_per_person(self,
                           person_id,
                           event_ids=None,
                           from_date='0000-01-01',
                           to_date='9999-12-31',
                           include_split_times=False,
                           top=None):
        """
        GET https://eventor.orientering.se/api/results/person
        Returnerar resultat för en person på ett antal tävlingar.

        Query-parametrar
        Namn Obl Standard Beskrivning
        personId   Person-id enligt /persons/organisations/{organisationId}.
        eventIds   Kommaseparerad lista med tävlings-id:n enligt /events. Utelämna för att inkludera alla tävlingar.
        fromDate  0000-01-01 Inkluderar tävlingar som arrangeras under detta eller senare datum (åååå-mm-dd).
        toDate  9999-12-31 Inkluderar tävlingar som arrangeras under detta eller tidigare datum (åååå-mm-dd).
        includeSplitTimes   Sätt till true för att inkludera sträcktider.
        top   Returnerar, förutom den angivna personen, endast detta antal deltagare från toppen av resultatlistan.
            Utelämna för att inkludera endast den angivna personen.
        Returnerat element

        ResultListList
        """
        if include_split_times:
            ist = 'true'
        else:
            ist = 'false'

        q = {'personId': person_id,
             'fromDate': from_date,
             'toDate': to_date,
             'includeSplitTimes': ist}

        if event_ids:
            q['eventIds'] = format_list(event_ids)
        if top:
            q['top'] = top
        try:
            return self._execute('results/person', q)['ResultListList']['ResultList']
        except TypeError:
            return []

    def results_per_organisation(self,
                                 organisation_id,
                                 event_id=None,
                                 include_split_times=False,
                                 top=None):
        """
        GET https://eventor.orientering.se/api/results/organisation
        Returnerar resultat för en organisations (klubbs) deltagare på en tävling.

        Query-parametrar
        Namn Obl Standard Beskrivning
        organisationIds ja  Kommaseparerad lista med id:n enligt /organisations för de organisationer som resultat ska
            hämtas för. Denna parameter måste sättas till den egna organisationens id.
        eventId   Tävlings-id enligt /events.
        includeSplitTimes   Sätt till true för att inkludera sträcktider.
        top   Returnerar, förutom de angivna organisationernas deltagare, endast detta antal deltagare från toppen av
            varje klass resultatlista. Utelämna för att inkludera endast de angivna organisationernas deltagare.
        Returnerat element

        ResultList
        """
        if include_split_times:
            ist = 'true'
        else:
            ist = 'false'

        q = {'organisationIds': format_list(organisation_id),
             'includeSplitTimes': ist}

        if event_id:
            q['eventId'] = event_id
        if top:
            q['top'] = top
        return self._execute('results/organisation', q)

    def activities(self, organisation_id, from_date='0000-01-01', to_date='9999-12-31', include_registrations=False):
        """
        GET https://eventor.orientering.se/api/activities
        Returnerar alla aktiviteter för en organisation (klubb) i en viss tidsperiod.

        Query-parametrar
        Namn Obl Standard Beskrivning
        organisationId ja  Organisationens id enligt /organisations. Denna parameter måste sättas till den egna
            organisationens id.
        from ja  Start för tidsperioden (åååå-mm-dd).
        to ja  Slut för tidsperioden (åååå-mm-dd).
        includeRegistrations  false Sätt till true för att inkludera anmälningar till aktiviteterna.
        Returnerat element

        ActivityList
        """
        if include_registrations:
            ir = 'true'
        else:
            ir = 'false'
        q = {'organisationId': organisation_id,
             'from': from_date,
             'to': to_date,
             'includeRegistrations': ir}
        return self._execute('activities', q)['ActivityList']['Activity']

    def activity(self, organisation_id, activity_id, include_registrations=False):
        """
        GET https://eventor.orientering.se/api/activity
        Returnerar en aktivitet.

        Query-parametrar
        Namn Obl Standard Beskrivning
        organisationId ja  Organisationens id enligt /organisations. Denna parameter måste sättas till den egna
            organisationens id.
        id ja  Aktivitetens id enligt /activities.
        includeRegistrations  false Sätt till true för att inkludera anmälningar till aktiviteten.
        Returnerat element

        Activity
        """
        if include_registrations:
            ir = 'true'
        else:
            ir = 'false'
        q = {'organisationId': organisation_id,
             'id': activity_id,
             'includeRegistrations': ir}
        return self._execute('activity', q)

    def competitor(self, person_id):
        """
        GET https://eventor.orientering.se/api/competitor/{personId}
        Returnerar en persons tävlingsuppgifter (t ex förvalda klasser och bricknummer).

        Path-parametrar
        Namn Obl Standard Beskrivning
        personId ja  Personens id enligt /persons/organisations/{organisationId}. Personen måste vara medlem i
            organisationen vars API-nyckel används.
        Returnerat element

        Competitor
        """
        return self._execute('competitor/{personId}'.format(person_id), None)
