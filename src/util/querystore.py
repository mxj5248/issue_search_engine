from datetime import date, timedelta,datetime
from util.redmine_feature_id_store import *
from util.query_generator import *

redmine_common_query_list = dict()

redmine_common_query_list['issues_d'] = build_query(
    ['id', 'description', 'tracker_id', 'project_id', 'status_id','subject','created_on','updated_on'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2020-01-01'},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리,pr_GS_CC인증,pr_platform)},
    {"column": 'tracker_id', "operator": In, "value":(tr_수정,tr_새기능,tr_버그,tr_요청)}])

redmine_common_query_list['journals_d'] = build_query(
    ['id', 'journalized_id', 'journalized_type', 'user_id', 'created_on'],
    ['journals'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-01-01'},
    {"column": 'journalized_type', "operator": Equal_str, "value":'issue'}])

redmine_common_query_list['journal_details_d'] = build_query(
    ['journal_id', 'property', 'prop_key', 'old_value', 'value'],
    ['journal_details'],
    [{"column": 'property', "operator": Not_Equal_str, "value":'attachment'},
     {"column": 'property', "operator": Not_Equal_str, "value":'relation'},
    {"column": 'prop_key', "operator": Not_Equal_str, "value":'assigned_to_id'}])

redmine_common_query_list['active_issues_d'] = build_query(
    ['id', 'tracker_id', 'project_id','subject', 'status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-01-01'},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리,pr_GS_CC인증,pr_platform,pr_요구사항정의)},
    {"column": 'status_id', "operator": In, "value":(st_신규,st_처리대기,st_처리중,st_설계중,st_기획완료,st_추가정보문의,st_추가정보답변,st_진행관련문의,st_진행관련문의답변,st_패치테스트중,st_패치테스트완료,st_고객사적용성공,st_고객사적용실패,st_패치배포,st_구현완료,st_복구지원중,st_복구지원완료,st_원인분석요청,st_원인분석완료,st_관리방안계획중,st_후속조치중)}])

redmine_common_query_list['active_issues_d2'] = build_query(
    ['id', 'tracker_id', 'project_id','subject', 'status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-01-01'},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리,pr_요구사항정의,pr_platform)},
    {"column": 'status_id', "operator": In, "value":(st_신규,st_처리대기,st_처리중,st_설계중,st_기획완료,st_구현완료,st_추가정보문의,st_추가정보답변,st_진행관련문의,st_진행관련문의답변,st_패치배포,st_패치테스트중,st_패치테스트완료,st_고객사적용실패,st_고객사적용성공)}])

this_month = (datetime.today()- timedelta(days=30)).strftime("%Y-%m-%d")
redmine_common_query_list['active_issues_tm_d'] = build_query(
    ['id', 'tracker_id', 'project_id','subject', 'status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value": this_month},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리,pr_GS_CC인증,pr_platform,pr_요구사항정의)},
    {"column": 'tracker_id', "operator": In, "value":(tr_수정,tr_새기능,tr_버그,tr_요청,tr_요구사항정의,tr_고객사장애)},
    {"column": 'status_id', "operator": In, "value":(st_신규,st_처리대기,st_처리중,st_설계중,st_기획완료,st_추가정보문의,st_추가정보답변,st_진행관련문의,st_진행관련문의답변,st_패치테스트중,st_패치테스트완료,st_고객사적용성공,st_고객사적용실패,st_패치배포,st_구현완료,st_복구지원중,st_복구지원완료,st_원인분석요청,st_원인분석완료,st_관리방안계획중,st_후속조치중)}])

redmine_common_query_list['request_day_d'] = build_query(
    ['customized_id', 'value'],
    ['custom_values'],
    [{"column": 'customized_type', "operator": Equal_str, "value":'Issue'},
    {"column": 'custom_field_id', "operator": Equal_num, "value":cf_요청완료일}
])

redmine_common_query_list['sites_name_d'] = build_query(
    ['customized_id', 'value'],
    ['custom_values'],
    [{"column": 'customized_type', "operator": Equal_str, "value":'Issue'},
    {"column": 'custom_field_id', "operator": Equal_num, "value":cf_사이트명}
])

redmine_common_query_list['close_issues_d'] = build_query(
    ['id', 'tracker_id', 'project_id','status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-01-01'},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리,pr_GS_CC인증,pr_platform,pr_요구사항정의)},
    {"column": 'status_id', "operator": Equal_num, "value":(st_처리완료)},
    {"column": 'status_id', "operator": Not_Equal_num, "value":(st_완료)}])

redmine_common_query_list['users_d'] = build_query(
    ['id', 'lastname', 'firstname','status', 'created_on', 'login'],
    ['users'],
    False)

redmine_common_query_list['userslogin_d'] = build_query(
    ['id', 'lastname', 'firstname','status', 'created_on', 'login'],
    ['users'],
    False)

redmine_common_query_list['group_of_users_d'] = build_query(
    ['group_id', 'user_id'],
    ['groups_users'],
    False)
    
previous_day = date.today() - timedelta(1)
redmine_common_query_list['previous_day_d'] = build_query(
    ['id', 'tracker_id', 'project_id','status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-01-01'},
     {"column": 'created_on', "operator": Less_than_equal, "value":str(previous_day)},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리,pr_GS_CC인증,pr_platform,pr_요구사항정의)},
    {"column": 'tracker_id', "operator": In, "value":(tr_수정,tr_새기능,tr_버그,tr_요청,tr_요구사항정의,tr_고객사장애)},
    {"column": 'status_id', "operator": In, "value":(st_신규,st_처리대기,st_처리중,st_설계중,st_기획완료,st_추가정보문의,st_추가정보답변,st_진행관련문의,st_진행관련문의답변,st_패치테스트중,st_패치테스트완료,st_고객사적용성공,st_고객사적용실패,st_패치배포,st_구현완료,st_복구지원중,st_복구지원완료,st_원인분석요청,st_원인분석완료,st_관리방안계획중,st_후속조치중)}])

redmine_common_query_list['last_oct_all_d'] = build_query(
    ['id', 'tracker_id', 'project_id','subject','status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2020-10-01'},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리,pr_GS_CC인증,pr_platform)},
    {"column": 'tracker_id', "operator": In, "value":(tr_수정,tr_새기능,tr_버그,tr_요청)},
    ])

redmine_common_query_list['journal_oct_all_d'] = build_query(
    ['id', 'journalized_id', 'journalized_type', 'user_id', 'created_on'],
    ['journals'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2020-10-01'},
    {"column": 'journalized_type', "operator": Equal_str, "value":'issue'}])

redmine_common_query_list['journal_details_status_d'] = build_query(
    ['journal_id', 'property', 'prop_key', 'old_value', 'value'],
    ['journal_details'],
    [{"column": 'property', "operator": Not_Equal_str, "value":'attachment'},
     {"column": 'property', "operator": Not_Equal_str, "value":'relation'},
    {"column": 'prop_key', "operator": Equal_str, "value":'status_id'}])

#Alarm
redmine_common_query_list['issues_a'] = build_query(
    ['id', 'tracker_id', 'project_id','subject','updated_on','status_id','priority_id','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-08-18'},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리)},
    {"column": 'tracker_id', "operator": In, "value":(tr_수정,tr_새기능,tr_버그)},
    {"column": 'status_id', "operator": In, "value":(st_구현완료,st_패치배포,st_처리완료,st_완료,st_테스트중,st_테스트완료,st_고객사적용성공,st_고객사적용실패,st_패치테스트중,st_패치테스트완료,st_결함보완대기)}])

redmine_common_query_list['journals_a'] = build_query(
    ['id', 'journalized_id', 'journalized_type', 'user_id', 'created_on'],
    ['journals'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-08-17'},
    {"column": 'journalized_type', "operator": Equal_str, "value":'issue'}])

redmine_common_query_list['journal_details_a1'] = build_query(
    ['journal_id', 'property', 'prop_key', 'old_value', 'value'],
    ['journal_details'],
    [{"column": 'property', "operator": Equal_str, "value":'cf'},
    {"column": 'prop_key', "operator": In, "value":(cf_설계내역,cf_구현내역)}])

redmine_common_query_list['request_day_a'] = build_query(
    ['customized_id', 'value'],
    ['custom_values'],
    [{"column": 'customized_type', "operator": Equal_str, "value":'Issue'},
    {"column": 'custom_field_id', "operator": Equal_num, "value":cf_요청완료일}
])

redmine_common_query_list['active_issues_a'] = build_query(
    ['id', 'tracker_id', 'project_id','subject', 'status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id','author_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-01-01'},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리,pr_GS_CC인증,pr_platform,pr_요구사항정의)},
    {"column": 'status_id', "operator": In, "value":(st_신규,st_처리대기,st_처리중,st_설계중,st_기획완료,st_추가정보문의,st_추가정보답변,st_진행관련문의,st_진행관련문의답변,st_패치테스트중,st_패치테스트완료,st_고객사적용성공,st_고객사적용실패,st_패치배포,st_구현완료,st_복구지원중,st_복구지원완료,st_원인분석요청,st_원인분석완료,st_관리방안계획중,st_후속조치중)}])

redmine_common_query_list['new_issues_a'] = build_query(
    ['id', 'tracker_id', 'project_id','subject', 'status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id','author_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-01-01'},
     {"column": 'tracker_id', "operator": In, "value":(tr_수정,tr_새기능,tr_버그,tr_요청,tr_요구사항정의,tr_고객사장애,tr_파트너사일감)},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리,pr_GS_CC인증,pr_platform,pr_요구사항정의,pr_구축요청사항정의,pr_국내파트너사일감등록)},
    {"column": 'status_id', "operator": Equal_num, "value":st_신규}])

redmine_common_query_list['journal_details_a2'] = build_query(
    ['journal_id', 'property', 'prop_key', 'old_value', 'value'],
    ['journal_details'],
    [{"column": 'property', "operator": Not_Equal_str, "value":'attachment'},
     {"column": 'property', "operator": Not_Equal_str, "value":'relation'},
    {"column": 'prop_key', "operator": Equal_str, "value":'assigned_to_id'}])

redmine_common_query_list['incorrect_assigned_name_a'] = build_query(
    ['id', 'tracker_id', 'project_id','subject', 'status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-01-01'},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리)},
    {"column": 'tracker_id', "operator": In, "value":(tr_수정,tr_새기능,tr_버그,tr_요청)},
    {"column": 'status_id', "operator": In, "value":(st_추가정보문의,st_추가정보답변 ,st_진행관련문의 ,st_진행관련문의답변 )}])

previous_time = datetime.today() - timedelta(hours=13)
redmine_common_query_list['active_issues_bf13hours_a'] = build_query(
    ['id', 'tracker_id', 'project_id','status_id','subject', 'created_on', 'updated_on', 'due_date','done_ratio','author_id','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-01-01'},
     {"column": 'created_on', "operator": Less_than_equal, "value":str(previous_time)},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리,pr_GS_CC인증,pr_platform,pr_요구사항정의,pr_국내파트너사일감등록)},
    {"column": 'tracker_id', "operator": In, "value":(tr_수정,tr_새기능,tr_버그,tr_요청,tr_요구사항정의,tr_고객사장애,tr_파트너사일감)},
    {"column": 'status_id', "operator": In, "value":(st_신규,st_처리대기,st_처리중,st_설계중,st_기획대기,st_기획완료,st_추가정보문의,st_추가정보답변,st_진행관련문의,st_진행관련문의답변,st_패치테스트중,st_패치테스트완료,st_고객사적용성공,st_고객사적용실패,st_패치배포,st_구현완료,st_복구지원중,st_복구지원완료,st_원인분석요청,st_원인분석완료,st_관리방안계획중,st_후속조치중)}])

redmine_common_query_list['issues_planned_a'] = build_query(
    ['id', 'tracker_id', 'project_id','subject', 'status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-01-01'},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리,pr_GS_CC인증)},
    {"column": 'tracker_id', "operator": In, "value":(tr_수정,tr_새기능,tr_버그,tr_요청)},
    {"column": 'status_id', "operator": Equal_num, "value":st_기획대기}])

redmine_common_query_list['issues_relation_a'] = build_query(
    ['id', 'issue_from_id', 'issue_to_id','relation_type'],
    ['issue_relations'],
    [{"column": 'relation_type', "operator": Equal_str, "value":'relates'}
   ])

redmine_common_query_list['all_planned_issues_a'] = build_query(
    ['id', 'tracker_id', 'project_id','subject', 'status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-01-01'},
    {"column": 'project_id', "operator": Equal_num, "value":pr_기획}])

redmine_common_query_list['issues_a2'] = build_query(
    ['id', 'tracker_id', 'project_id','subject', 'status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-01-01'},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리,pr_GS_CC인증)},
    {"column": 'tracker_id', "operator": In, "value":(tr_수정,tr_새기능,tr_버그,tr_요청)}])

redmine_common_query_list['inco_assgner_issues'] = build_query(
    ['id', 'tracker_id', 'project_id','subject', 'status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2021-08-17'},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리)},
    ])

redmine_common_query_list['unfilled_info_issues'] = build_query(
    ['id', 'tracker_id', 'project_id','subject', 'status_id', 'created_on', 'updated_on', 'root_id','parent_id','due_date','author_id','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2022-01-01'},
    {"column": 'project_id', "operator": Equal_num, "value":(pr_국내파트너사일감등록)},
    {"column": 'status_id', "operator": In, "value":(st_신규,st_처리대기,st_처리중,st_추가정보문의,st_추가정보답변,st_진행관련문의,st_진행관련문의답변,st_고객사적용성공,st_고객사적용실패)}])

redmine_common_query_list['all_issues'] = build_query(
    ['id', 'tracker_id', 'project_id','status_id', 'created_on', 'updated_on', 'done_ratio','assigned_to_id'],
    ['issues'],
    False)

redmine_common_query_list['custom_values'] = build_query(
    ['customized_id', 'custom_field_id', 'value'],
    ['custom_values'],
    False)

redmine_common_query_list['version_info_issues'] = build_query(
    ['id', 'tracker_id', 'project_id','subject','updated_on','priority_id','assigned_to_id','fixed_version_id','due_date'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2022-01-17'},
     {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리)},
    {"column": 'status_id', "operator": In, "value":(st_완료,st_테스트완료)}])


redmine_common_query_list['alerts_issues'] = build_query(
    ['id', 'tracker_id', 'project_id','status_id','subject', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2022-01-01'},
    {"column": 'project_id', "operator": In, "value":(pr_이슈관리,pr_요구사항정의)},
    {"column": 'tracker_id', "operator": In, "value":(tr_요구사항정의,tr_고객사장애)},
    {"column": 'status_id', "operator": In, "value":(st_신규,st_처리대기,st_처리중,st_보류,st_설계중,st_기획완료,st_추가정보문의,st_추가정보답변,st_진행관련문의,st_진행관련문의답변,st_패치테스트중,st_패치테스트완료,st_고객사적용성공,st_고객사적용실패,st_패치배포,st_구현완료,st_복구지원중,st_복구지원완료,st_원인분석요청,st_원인분석완료,st_관리방안계획중,st_후속조치중)}])

redmine_common_query_list['alerts_com_issues'] = build_query(
    ['id', 'tracker_id', 'project_id','status_id','subject', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2022-01-01'},
    {"column": 'project_id', "operator": In, "value":(pr_이슈관리,pr_요구사항정의)},
    {"column": 'tracker_id', "operator": In, "value":(tr_요구사항정의,tr_고객사장애,tr_고객사긴급)},
    {"column": 'status_id', "operator": In, "value":(st_신규,st_처리대기,st_처리중,st_보류,st_설계중,st_완료,st_기획완료,st_추가정보문의,st_추가정보답변,st_진행관련문의,st_진행관련문의답변,st_패치테스트중,st_패치테스트완료,st_고객사적용성공,st_고객사적용실패,st_패치배포,st_구현완료,st_복구지원중,st_복구지원완료,st_원인분석요청,st_원인분석완료,st_관리방안계획중,st_후속조치중,st_긴급지원완료)}])

redmine_common_query_list['unsync_issues'] = build_query(
    ['id', 'tracker_id', 'project_id','subject', 'status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2022-03-14'},
    {"column": 'project_id', "operator": In, "value":(pr_표준패키지,pr_이슈관리)}
    ])

redmine_common_query_list['partners_issues'] = build_query(
    ['id', 'tracker_id', 'project_id','subject', 'status_id', 'created_on', 'updated_on', 'due_date','done_ratio','assigned_to_id','author_id'],
    ['issues'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2022-01-01'},
    {"column": 'project_id', "operator": Equal_num, "value":(pr_국내파트너사일감등록)},
    {"column": 'tracker_id', "operator": In, "value":(tr_파트너사장애,tr_파트너사긴급)},
    {"column": 'done_ratio', "operator": Not_Equal_num, "value": 100},
    ])

redmine_common_query_list['journals_partners'] = build_query(
    ['id', 'journalized_id', 'journalized_type', 'user_id', 'created_on'],
    ['journals'],
    [{"column": 'created_on', "operator": Greater_than_equal, "value":'2022-01-01'},
    {"column": 'journalized_type', "operator": Equal_str, "value":'issue'}])

redmine_common_query_list['journal_details_partners'] = build_query(
    ['journal_id', 'property', 'prop_key', 'old_value', 'value'],
    ['journal_details'],
    [{"column": 'property', "operator": Not_Equal_str, "value":'attachment'},
     {"column": 'property', "operator": Not_Equal_str, "value":'relation'},
    {"column": 'prop_key', "operator": Not_Equal_str, "value":'assigned_to_id'}])

redmine_common_query_list['email_query'] = build_query(
    ['user_id', 'address'],
    ['email_addresses'],
    False)