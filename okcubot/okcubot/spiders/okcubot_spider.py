# -*- coding: UTF-8 -*-
from scrapy.spider import Spider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy import log

import re

from okcubot.items import UserItem, QuestionItem, AnswerItem

class OkCubotSpider(Spider):
    # Spider settings
    name = "okcubot"

    # Others
    base_url = "http://www.okcupid.com"

    user_queue = []

    # TODO: Implement missing traits
    personality_scale_dict = {
        'p_explove': re.compile('(experienced in love)', re.IGNORECASE),
        'p_adven': re.compile('(adventurous)', re.IGNORECASE),
        'p_indie': re.compile('(indie)', re.IGNORECASE),
        'p_spon': re.compile('(spontaneous)', re.IGNORECASE),
        'p_scien': re.compile('(scientific)', re.IGNORECASE),
        'p_inde': re.compile('(independent)', re.IGNORECASE),
        'p_conf': re.compile('(confident)', re.IGNORECASE),
        'p_math': re.compile('(mathematical)', re.IGNORECASE),
        'p_logic': re.compile('(logical)', re.IGNORECASE),
        'p_organ': re.compile('(organized)', re.IGNORECASE),
        'p_oldfash': re.compile('(old\-fashioned)', re.IGNORECASE),
        'p_lit': re.compile('(literary)', re.IGNORECASE),
        'p_opti': re.compile('(optimistic)', re.IGNORECASE),
        'p_roman': re.compile('(romantic)', re.IGNORECASE),
        'p_comp': re.compile('(compassionate)', re.IGNORECASE),
        'p_lovedri': re.compile('(love\-driven)', re.IGNORECASE),
        'p_sprit': re.compile('(spiritual)', re.IGNORECASE),
        'p_kinky': re.compile('(kinky)', re.IGNORECASE),
        'p_artsy': re.compile('(artsy)', re.IGNORECASE),
        'p_thrift': re.compile('(thrifty)', re.IGNORECASE),
        'p_drug': re.compile('(drug\-friendly)', re.IGNORECASE),
        'p_arro': re.compile('(arrogant)', re.IGNORECASE),
        'p_sloppy': re.compile('(sloppy)', re.IGNORECASE),
        'p_extro': re.compile('(extroverted)', re.IGNORECASE),
        'p_geeky': re.compile('(geeky)', re.IGNORECASE),
        'p_aggre': re.compile('(aggressive)', re.IGNORECASE),
        'p_expsex': re.compile('(experienced in sex)', re.IGNORECASE),
        'p_capi': re.compile('(capitalistic)', re.IGNORECASE),
        'p_exer': re.compile('(into exercise)', re.IGNORECASE),
        'p_kind': re.compile('(kind)', re.IGNORECASE),
        'p_pure': re.compile('(pure)', re.IGNORECASE),
        'p_convenmoral': re.compile('(conventionally moral)', re.IGNORECASE),
        'p_manners': re.compile('(mannered)', re.IGNORECASE),
        'p_ambi': re.compile('(ambitious)', re.IGNORECASE),
        'p_polit': re.compile('(political)', re.IGNORECASE),
        'p_greed': re.compile('(greedy)', re.IGNORECASE),
        'p_sexdrive': re.compile('(sex\-driven)', re.IGNORECASE),
        'p_energetic': re.compile('(energetic)', re.IGNORECASE),
        'p_cool': re.compile('(cool)', re.IGNORECASE),
        'p_introvert': re.compile('(introverted)', re.IGNORECASE),
        'p_trusting': re.compile('(trusting)', re.IGNORECASE),
        'p_dominant': re.compile('(dominant)', re.IGNORECASE),
        'p_laidback': re.compile('(laid\-back)', re.IGNORECASE),
        'p_submissive': re.compile('(submissive)', re.IGNORECASE),
        'p_explife': re.compile('(experienced in life)', re.IGNORECASE),
        'p_friendstrangers': re.compile('(friendly to strangers)', re.IGNORECASE),
        'p_honest': re.compile('(honest)', re.IGNORECASE),
        'p_giving': re.compile('(giving)', re.IGNORECASE),
        'p_passion': re.compile('(passion\-driven)', re.IGNORECASE),
        'p_progress': re.compile('(progressive)', re.IGNORECASE)
    }

    # Regular expressions
    education_re = re.compile('(graduated from|working on|dropped out of|)\s?(high school|university|masters program|law school|med school|space camp|ph\.d program|two\-year college)', re.IGNORECASE)
    lf_age_re = re.compile('(\d+).(\d+)')

    # User
    user = None
    password = None

    # Seeds and target
    target = None

    # Args
    #   user - username for bot account
    #   pass - password for bot account
    #   target - optional target for scraping single users
    def __init__(self, *args, **kwargs):
        super(OkCubotSpider, self).__init__(*args, **kwargs)

        if "user" not in kwargs or "pass" not in kwargs:
            print "Please supply a user and a password"
            exit()

        if "target" in kwargs:
            self.target = kwargs['target']

        self.user = kwargs['user']
        self.password = kwargs['pass']

        # Patch
        self.monkey_patch_HTTPClientParser_statusReceived()

    def spider_idle(self, spider):
        next_user = self.next_user()
        if next_user is not None:
            yield next_user

    def queue_user(self, req):
        if req not in self.user_queue:
            if len(self.user_queue) < 100:
                self.user_queue.append(req)
                return True
            else:
                log.msg('User queue is too big. Skipping.')
                return False

        log.msg('User is already in queue. Skipping.')
        return False


    def next_user(self):
        if len(self.user_queue) > 0:
            return self.user_queue.pop()
        return None

    def start_requests(self):
        return [FormRequest("https://www.okcupid.com/login",
                            formdata={'username': self.user, 'password': self.password},
                            callback=self.logged_in)]

    def logged_in(self, response):
        selector = Selector(response)

        if self.target != None:
            # We only want to scrape this user
            yield Request(self.base_url + '/profile/' + self.target, callback=self.parse_profile)
        else:
            profiles = selector.css('#similar_users_list li > a::attr(href), #matchphotobrowser_int .item a.name::attr(href)').extract()
            if len(profiles) == 0:
                log.msg('Credentials incorrect.', level=log.ERROR)
            else:
                for url in profiles:
                    log.msg('Seeded bot with user (' + url + ')')
                    self.queue_user(Request(self.base_url + url, callback=self.parse_profile))

        # Yield two users to get things started
        yield self.next_user()
        yield self.next_user()

    def parse_profile(self, response):
        selector = Selector(response)

        # TODO: Implement
        #       d_pets_dogs = Field()
        #       d_pets_cats = Field()

        attribute_dict = {
            # Details
            'd_username': '#basic_info_sn.name::text',
            'd_age': '#ajax_age::text',
            'd_gender': '.ajax_gender::text',
            'd_orientation': '#ajax_orientation::text',
            'd_ethnicity': '#ajax_ethnicities::text',
            'd_bodytype': '#ajax_bodytype::text',
            'd_relationship': '#ajax_status::text',
            'd_smokes': '#ajax_smoking::text',
            'd_drinks': '#ajax_drinking::text',
            'd_drugs': '#ajax_drugs::text',
            'd_languages': '#ajax_languages::text',
            'd_job': '#ajax_job::text',
            'd_income': '#ajax_income::text',

            # Looking for
            'lf_location': '#ajax_near::text',
            'lf_want': '#ajax_gentation::text',
            'lf_single': '#ajax_single::text'
        }

        user = UserItem()
        # Iterate over attribute dictionary and fetch data
        for attr, ident in attribute_dict.iteritems():
            val = selector.css(ident).extract()[0]

            # Translate - to blanks
            val = val.encode('utf-8').replace('—', '')

            # Set attribute
            user[attr] = val

        # Looking for
        user['lf_for'] = selector.css('#ajax_lookingfor::text').extract()[0].replace('for', '')

        age = selector.css('#ajax_ages::text').extract()[0]
        age = self.lf_age_re.findall(age)
        lf_min_age = None
        lf_max_age = None
        if len(age) > 0:
            # Stored in tuples.. appearantly
            lf_min_age = age[0][0]
            lf_max_age = age[0][1]
        user['lf_min_age'] = lf_min_age
        user['lf_max_age'] = lf_max_age

        # Location
        location = selector.css('#ajax_location::text').extract()[0].split(',')
        city = location[0]
        country = location[1]
        user['d_city'] = city
        user['d_country'] = country

        # Diet
        diet = selector.css('#ajax_diet::text').extract()[0].split(' ')
        diet_manner = None
        diet_type = None
        if len(diet) == 1:
            diet_type = diet[0]
        elif len(diet) == 2:
            diet_manner = diet[0]
            diet_type = diet[1]
        user['d_diet_manner'] = diet_manner
        user['d_diet_type'] = diet_type

        # Religion
        religion = selector.css('#ajax_religion::text').extract()[0].split(',')
        religion_type = None
        religion_seriosity = None
        if len(religion) == 1:
            religion_type = religion[0]
        elif len(religion) == 2:
            religion_type = religion[0]
            religion_seriosity = religion[1]
        user['d_religion_type'] = religion_type
        user['d_religion_seriosity'] = religion_seriosity

        # Astrology
        astrology = selector.css('#ajax_sign::text').extract()[0].split(',')
        astrology_sign = None
        astrology_seriosity = None
        if len(astrology) == 1:
            astrology_sign = astrology[0]
        elif len(astrology) == 2:
            astrology_sign = astrology[0]
            astrology_seriosity = astrology[1]
        user['d_astrology_sign'] = astrology_sign
        user['d_astrology_seriosity'] = astrology_seriosity

        # Relationship
        relationship = selector.css('#ajax_monogamous::text').extract()[0].split(' ')
        relationship_manner = None
        relationship_type = None
        if len(relationship) == 1:
            relationship_type = relationship[0]
        elif len(relationship) == 2:
            relationship_manner = relationship[0]
            relationship_type = relationship[1]
        user['d_relationship_manner'] = relationship_manner
        user['d_relationship_type'] = relationship_type

        # Offspring
        offspring = selector.css('#ajax_children::text').extract()[0].split(' ')
        offspring_desires = None
        offspring_current = None
        if len(offspring) == 1:
            offspring_current = offspring[0]
        elif len(offspring) == 2:
            offspring_desires = offspring[0]
            offspring_current = offspring[1]
        user['d_offspring_desires'] = offspring_desires
        user['d_offspring_current'] = offspring_current

        # Education
        education = selector.css('#ajax_education::text').extract()[0]
        education = self.education_re.findall(education)
        education_phase = None
        education_type = None
        if len(education) > 0:
            # Stored in tuples.. appearantly
            education_phase = education[0][0]
            education_type = education[0][1]
        user['d_education_type'] = education_type
        user['d_education_phase'] = education_phase

        # Trim values
        for attr, val in user.iteritems():
            if val is not None:
                user[attr] = val.strip()

        # Request parsing of the user's personality traits
        request = Request(self.base_url + '/profile/' + user['d_username'] + '/personality', callback=self.parse_personality, priority=100)
        request.meta['user'] = user
        yield request

        if self.target == None:
            # Find other users
            i = 0
            for url in selector.css('#similar_users_list li > a::attr(href), .match > a::attr(href)').extract():
                if url != response.request.url:
                    if self.queue_user(Request(self.base_url + url, callback=self.parse_profile, priority=-100)):
                        i += 1
            log.msg('Queued ' + `i` + ' users from ' + user['d_username'] + ' (' + str(len(self.user_queue)) + ')')

    def parse_personality(self, response):
        selector = Selector(response)

        user = response.meta['user']

        i = 0
        for trait in selector.css('.pt_row'):
            label = trait.css('label::text').extract()[0]
            percentage = re.sub('(width\:)|(\%\;)', '', trait.css('span::attr(style)').extract()[0])

            try:
                percentage = int(percentage)
            except ValueError:
                log.msg('Could not parse trait, moving on.', level=log.ERROR)
                continue

            if len(trait.css('p.right > label')) == 1:
                # Label is in right p, so negate the percentage
                percentage = -percentage

            actual = None
            for t, r in self.personality_scale_dict.iteritems():
                if r.search(label):
                    actual = t

            if actual == None:
                log.msg('Unknown trait ' + label, level=log.ERROR)
            else:
                user[actual] = percentage
                i += 1
        log.msg(`i` + ' traits parsed for user ' + user['d_username'])

        # Request parsing questions/answers
        request = Request(self.base_url + '/profile/' + user['d_username'] + '/questions', callback=self.parse_questions, priority=400)
        request.meta['user'] = user
        yield request

    def parse_questions(self, response):
        selector = Selector(response)

        user = response.meta['user']

        i = 0
        for qa in selector.css('.question'):
            i += 1

            qid = qa.css('::attr(data-qid)').extract()[0]
            if qa.css('.not_answered'):
                # Not answered, answer it and store it.
                question = QuestionItem()
                question['id'] = qid
                question['text'] = qa.css('.qtext > p::text').extract()[0].strip()
                options = qa.css('.my_answer > label::text').extract()

                if len(options) > 0:
                    question['option_1'] = options[0].strip()
                if len(options) > 1:
                    question['option_2'] = options[1].strip()
                if len(options) > 2:
                    question['option_3'] = options[2].strip()
                if len(options) > 3:
                    question['option_4'] = options[3].strip()

                # TODO: Make the bot actually answer the question
                #yield self.answer_question(qid, 1)
                yield question
            else:
                answer = AnswerItem()
                answer['author'] = user['d_username']
                answer['question'] = qid
                answer['answer'] = qa.css('.answers .target .text::text').extract()[0].strip()
                answer['answer_text'] = qa.css('.answers .target .note::text').extract()[0].strip()

                yield answer

        log.msg(`i` + ' questions/answers parsed for user ' + user['d_username'])

        if len(selector.css('.pages .next.disabled').extract()) > 0:
            # We don't have any more pages. Yield the user.
            log.msg('Done processing ' + user['d_username'])
            yield user

            next_user = self.next_user()
            if next_user is None:
                log.msg('No more users in queue.')
            else:
                yield next_user
        else:
            # We're not done.
            next = selector.css('.pages .next > a::attr(href)').extract()[0]
            request = Request(self.base_url + next, callback=self.parse_questions, priority=400)
            request.meta['user'] = user
            yield request

    # FIXME: ?
    def answer_question(self, qid, option):
        return FormRequest("https://www.okcupid.com/questions/ask",
                            formdata={
                                'ajax': '1',
                                'submit': '1',
                                'answer_question': '1',
                                'skip': '0',
                                'show_all': '0',
                                'is_new': '1',
                                'matchanswers': 'irrelevant',
                                'qid': str(qid),
                                'importance': '5',
                                'is_public': '1',
                                'note': '',
                                'delete_note': '0',
                                'targetid': '',
                                'is_public': '1',
                                'answers': str(option)
                            },
                            callback=self.answered, priority=1000,
                            headers={
                                'Accept': 'application/json',
                                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                'X-Requested-With': 'XMLHttpRequest'
                            })

    # TODO: implement(?)
    def answered(self, response):
        # TODO: WE NEED TO GET THEIR ANSWER (hint: target in POST)
        pass

    def monkey_patch_HTTPClientParser_statusReceived(self):
        """
        Monkey patch for twisted.web._newclient.HTTPClientParser.statusReceived
        """
        from twisted.web._newclient import HTTPClientParser, ParseError
        old_sr = HTTPClientParser.statusReceived
        def statusReceived(self, status):
            try:
                return old_sr(self, status)
            except ParseError, e:
                if e.args[0] == 'wrong number of parts':
                    log.msg('Wrong number of parts in header. Assuming 200 OK', level=log.DEBUG)
                    return old_sr(self, str(status) + ' OK')
                raise
                statusReceived.__doc__ == old_sr.__doc__
        HTTPClientParser.statusReceived = statusReceived
