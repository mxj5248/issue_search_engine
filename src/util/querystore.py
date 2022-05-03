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

redmine_common_query_list['portal_d'] = '''
SELECT IDT.ISSUE_DATA_NUM AS issue_data_num,
	NIDT.TITLE AS title,
	F.VALUE AS content,
	IF(DIT.NAME IS NULL OR DIT.NAME = '' , DIT2.NAME, DIT.NAME) AS issue_type,
	DST.NAME AS site_name,
	DIGT.TITLE as biz_title,
	DUT.NAME AS issue_manage_user,
	IDT.REG_DT AS create_on
FROM
	NADPORTAL_IDX_DEFAULT_TB NIDT 
  INNER JOIN ISSUE_DATA_TB IDT ON	NIDT.ISSUE_DATA_UID = IDT.UID
	INNER JOIN DEF_SITE_TB DST ON IDT.SITE_UID = DST.UID
  INNER JOIN BIZ_INFO_TB BIT ON IDT.BIZ_UID = BIT.UID
	INNER JOIN DEF_ISSUE_GROUP_TB DIGT ON DIGT.UID = BIT.ISSUE_GROUP_UID
  LEFT OUTER JOIN DEF_ISSUE_TB DIT ON IDT.ISSUE_UID = DIT.UID
	LEFT OUTER JOIN DEF_ISSUE_TB DIT2 ON IDT.ISSUE_TEMPLATE_UID = DIT2.UID
  INNER JOIN (
  			SELECT * FROM (
					SELECT 
							DIT.UID as uid,		
							DIT.NAME as name,
							DIT.ISSUE_ID as issueId
						FROM 
							DEF_ISSUE_TB DIT LEFT OUTER JOIN DEF_ISSUE_GROUP_TB DIGT
							ON DIT.ISSUE_GROUP_UID = DIGT.UID
							LEFT OUTER JOIN DEF_ISSUE_TB DIT2
							ON DIT.TEMPLATE_UID = DIT2.UID
						WHERE
							DIT.PARENT_UID IN (SELECT UID FROM DEF_ISSUE_TB DIT3 WHERE DIT3.NAME IN ('SR','구축'))
							AND DIT.USE_GB = 'DATA'
					UNION ALL 
					SELECT 
							UID, 
							NAME, 
							ISSUE_ID 
						FROM 
							DEF_ISSUE_TB dit4 
						WHERE 
							NAME IN ('SR', '라이선스', '구축')
				) A 
				GROUP BY UID, NAME, ISSUEID
			) T ON IDT.ISSUE_UID = T.UID
	LEFT OUTER JOIN DEF_USER_TB DUT ON NIDT.ISSUE_MANAGE_USER = DUT.UID 
  LEFT OUTER JOIN (
  				SELECT 
  						IFDT.ISSUE_DATA_UID, 
  						IFDT.VALUE 
					FROM 
						ISSUE_FIELD_DATA_TB IFDT LEFT OUTER JOIN DEF_FIELD_TB DFT ON IFDT.FIELD_UID = DFT.UID 
					WHERE 
						DFT.FIELD_KEY = 'CONTENT'
  				) F ON NIDT.ISSUE_DATA_UID = F.ISSUE_DATA_UID'''