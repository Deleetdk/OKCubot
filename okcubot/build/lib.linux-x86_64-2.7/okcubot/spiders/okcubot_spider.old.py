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

    # User
    user = None
    password = None

    # Seeds and target
    target = None

    # TODO: Format argument in constructor
    # Args
    #   user - username for bot account
    #   pass - password for bot account
    #   target - optional target for scraping single users
    #   format - optional (default: tsv) format to export data to (e.g. csv, tsv)
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
            profiles = selector.css('#similar_users_list li > a::attr(href), .match > a::attr(href)').extract()
            if len(profiles) == 0:
                log.msg('Credentials incorrect.', level=log.ERROR)
            else:
                for url in profiles:
                    log.msg('Seeded bot with user (' + url + ')')
                    yield Request(self.base_url + url, callback=self.parse_profile)

    def parse_profile(self, response):
        selector = Selector(response)

        # TODO: Handle parameters which are - as none.
        # A note on this is that you can set default values
        # etc. in the Field method of an item.
        # TODO: Trim
        # TODO: Implement
        #       d_religion_type = Field()
        #       d_religion_seriosity = Field()
        #       d_astrology_sign = Field()
        #       d_astrology_seriosity = Field()
        #       d_education_phase = Field()
        #       d_education_type = Field()
        #       d_job = Field()
        #       d_income = Field()
        #       d_relationship = Field()
        #       d_relationship_manner = Field()
        #       d_relationship_type = Field()
        #       d_offspring_current = Field()
        #       d_offspring_desires = Field()
        #       d_pets_dogs = Field()
        #       d_pets_cats = Field()
        #   Looking for
        #       lf_want = Field()
        #       lf_min_age = Field()
        #       lf_max_age = Field()
        #       lf_location = Field()
        #       lf_single = Field()
        #       lf_for = Field()

        attribute_dict = {
            'd_username': '#basic_info_sn.name::text',
            'd_age': '#ajax_age::text',
            'd_gender': '.ajax_gender::text',
            'd_orientation': '#ajax_orientation::text',
            'd_ethnicity': '#ajax_ethnicities::text',
            'd_bodytype': '#ajax_bodytype::text',
            'd_smokes': '#ajax_smoking::text',
            'd_drinks': '#ajax_drinking::text',
            'd_drugs': '#ajax_drugs::text',
            'd_languages': '#ajax_languages::text',
        }

        user = UserItem()
        # Iterate over attribute dictionary and fetch data
        for attr, ident in attribute_dict.iteritems():
            val = selector.css(ident).extract()[0]

            # Trim
            val = val.strip()

            # Translate - to blanks
            val = val.replace('—', '')

            # Set attribute
            user[attr] = val

        #name = selector.css('#basic_info_sn.name::text').extract()[0]

        #age = selector.css('#ajax_age::text').extract()[0]
        #gender = selector.css('.ajax_gender::text').extract()[0]
        location = selector.css('#ajax_location::text').extract()[0].split(',')
        city = location[0]
        country = location[1]
        #orientation = selector.css('#ajax_orientation::text').extract()[0]
        #ethnicity = selector.css('#ajax_ethnicities::text').extract()
        #bodytype = selector.css('#ajax_bodytype::text').extract()[0]
        diet = selector.css('#ajax_diet::text').extract()[0].split(' ')
        # Diet handling stuff
        diet_manner = 0
        diet_type = 0
        if len(diet) == 1:
            diet_type = diet[0]
        else:
            diet_manner = diet[0]
            diet_type = diet[1]
        # End diet handling stuff
        #smokes = selector.css('#ajax_smoking::text').extract()[0]
        #drinks = selector.css('#ajax_drinking::text').extract()[0]
        #drugs = selector.css('#ajax_drugs::text').extract()[0]
        
        #user['d_username'] = name
        #user['d_age'] = age
        #user['d_gender'] = gender
        user['d_city'] = city
        user['d_country'] = country
        #user['d_orientation'] = orientation
        #user['d_ethnicity'] = ethnicity # TODO: fix
        #user['d_bodytype'] = bodytype
        user['d_diet_manner'] = diet_manner
        user['d_diet_type'] = diet_type
        #user['d_smokes'] = smokes
        #user['d_drinks'] = drinks
        #user['d_drugs'] = drugs

        # Request parsing of the user's personality traits
        request = Request(self.base_url + '/profile/' + name + '/personality', callback=self.parse_personality, priority=100)
        request.meta['user'] = user
        yield request

        if self.target == None:
            # Find other users
            i = 0
            for url in selector.css('#similar_users_list li > a::attr(href), .match > a::attr(href)').extract():
                i += 1
                if url != response.request.url:
                    yield Request(self.base_url + url, callback=self.parse_profile, priority=-100)
            log.msg('Queued ' + `i` + ' users from ' + name)

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
                question['text'] = qa.css('.qtext > p::text').extract()[0]
                options = qa.css('.my_answer > label::text').extract()

                if len(options) > 0:
                    question['option_1'] = options[0]
                if len(options) > 1:
                    question['option_2'] = options[1]
                if len(options) > 2:
                    question['option_3'] = options[2]
                if len(options) > 3:
                    question['option_4'] = options[3]

                # TODO: Make the bot actually answer the question
                #yield self.answer_question(qid, 1)
                yield question
            else:
                answer = AnswerItem()
                answer['author'] = user['d_username']
                answer['question'] = qid
                answer['answer'] = qa.css('.answers .target .text::text').extract()[0]
                answer['answer_text'] = qa.css('.answers .target .note::text').extract()[0]

                yield answer

        log.msg(`i` + ' questions/answers parsed for user ' + user['d_username'])

        if len(selector.css('.pages .next.disabled').extract()) > 0:
            # We don't have any more pages. Yield the user.
            log.msg('Done processing ' + user['d_username'])
            yield user
        else:
            # We're not done.
            next = selector.css('.pages .next > a::attr(href)').extract()[0]
            request = Request(self.base_url + next, callback=self.parse_questions, priority=400)
            request.meta['user'] = user
            yield request

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