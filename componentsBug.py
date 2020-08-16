#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2020/8/15 20:48
#@Author: Yuanqing Mei
#@Email: dg1533019@smail.nju.edu.cn
#@File  : jira.py

'''
封装jira一些方法
'''

from jira import JIRA
import sys
import os
import csv


class JiraTool():
    def __init__(self, server, username, password, maxResults = 500):
        self.server = server
        self.basic_auth = (username, password)
        # issues查询的最大值
        self.maxResults = maxResults

    def login(self):
        self.jira = JIRA(server=self.server, basic_auth=self.basic_auth)
        if self.jira == None:
            print('连接失败')
            sys.exit(-1)

    def get_projects(self):
        """
        获得jira 的所有项目
        :return:
        """
        return [(p.key, p.name, p.id) for p in self.jira.projects()]

    def get_components(self, project):
        """
        获得某项目的所有模块
        :param project:
        :return:
        """
        return [(c.name, c.id) for c in self.jira.project_components(self.jira.project(project))]

    def create_component(self, project, compoment, description, leadUserName=None, assigneeType=None,
                         isAssigneeTypeValid=False):
        """
        # 创建项目模块
        :param project: 模块所属项目
        :param compoment:模块名称
        :param description:模块描述
        :param leadUserName:
        :param assigneeType:
        :param isAssigneeTypeValid:
        :return:
        """
        components = self.jira.project_components(self.jira.project(project))
        if compoment not in [c.name for c in components]:
            self.jira.create_component(compoment, project, description=description, leadUserName=leadUserName,
                                       assigneeType=assigneeType, isAssigneeTypeValid=isAssigneeTypeValid)

    def create_issue(self, project, compoment, summary, description, assignee, issuetype, priority='Medium'):
        """
        创建提交bug
        :param project: 项目
        :param issuetype: 问题类型，Task
        :param summary: 主题
        :param compoment: 模块
        :param description: 描述
        :param assignee: 经办人
        :param priority: 优先级
        :return:
        """
        issue_dict = {
            'project': {'key': project},
            'issuetype': {'id': issuetype},
            'summary': summary,
            'components': [{'name': compoment}],
            'description': description,
            'assignee': {'name': assignee},
            'priority': {'name': priority},
        }
        return self.jira.create_issue(issue_dict)

    def delete_issue(self, issue):
        """
        删除bug
        :param issue:
        :return:
        """
        issue.delete()

    def update_issue_content(self, issue, issue_dict):
        """
        更新bug内容
        :param issue:
        :param issue_dict:
            issue_dict = {
                'project': {'key': project},
                'issuetype': {'id': issuetype},
                'summary': summary,
                'components': [{'name': compoment}],
                'description': description,
                'assignee': {'name': assignee},
                'priority': {'name': priority},
            }
        :return:
        """
        issue.update(fields=issue_dict)
    def update_issue_issuetype(self, issue, issuetype):
        """
        更新bug 状态
        :param issue:
        :param issuetype: 可以为id值如11，可以为值如'恢复开启问题'
        :return:
        """
        transitions = self.jira.transitions(issue)
        # print([(t['id'], t['name']) for t in transitions])
        self.jira.transition_issue(issue, issuetype)

    def search_issues(self, jql):
        """
        查询bug
        :param jql: 查询语句，
                    如"project=项目key AND component = 模块 AND status=closed AND summary ~标题 AND description ~描述"
        :return:
        """
        try:
            # maxResults参数是设置返回数据的最大值，默认是50。
            issues = self.jira.search_issues(jql, maxResults=self.maxResults)
        except Exception as e:
            print(e)
            sys.exit(-1)
        return issues
    def search_issue_content(self, issue, content_type):
        """
        获取bug 的相关信息
        :param issue:
        :param content_type:项目project; 模块名称components; 标题summary; 缺陷类型issuetype; 具体描述内容description;
                            经办人assignee; 报告人reporter; 解决结果resolution; bug状态status; 优先级priority;
                            创建时间created; 更新时间updated; 评论comments
        :return:
        """
        # 评论
        if content_type == 'comments':
            return [c.body for c in self.jira.comments(issue)]
        if hasattr(issue.fields, content_type):
            result = getattr(issue.fields, content_type)
            if isinstance(result, list):
                return [c.name for c in result if hasattr(c, 'name')]
            return result

    def collect_bug_report(self, project, root_path):
        """
        搜集bug报告上模块信息
        :param project:
        :param root_path:
        :return:
        """
        import os
        # jira = JIRA(server="https://issues.apache.org/jira/")

        statistics_path = root_path + '/BugReport/statistics/'
        reports_path = root_path + '/BugReport/reports/' + project + '/'
        if not os.path.exists(statistics_path):
            os.makedirs(statistics_path)
        if not os.path.exists(reports_path):
            os.makedirs(reports_path)

        text = 'id, Key, Type, Status, Resolution, Priority, components, AffectsVersions, FixedVersions, Reporter, ' \
               'Creator, Assignee, CreatedDate, ResolutionDate, UpdatedDate, Summary\n'
        search_str = 'project = ' + project.upper() + ' AND issuetype = Bug AND status in (Resolved, Closed) AND ' \
                                                      'resolution in (Fixed, Resolved) ORDER BY key ASC'

        start = 0
        max_results_each_search = 1000
        while True:
            try:
                # maxResults参数是设置返回数据的最大值，默认是50。
                issues = self.jira.search_issues(search_str, startAt=start, maxResults=max_results_each_search)
            except Exception as e:
                print(e)
                sys.exit(-1)
            # issues = jira.search_issues(search_str, startAt=start, maxResults=max_results_each_search)
            # print("the issues is ", issues)
            # for issue in issues:
            #     print(issue.fields.versions)
            #     print(issue.fields.versions, '              ',
            #           issue.fields.components[0] if len(issue.fields.components) > 0 else 'this is null')
            #     print(issue.fields.summary)
            for issue in issues:
                text += issue.id + ','
                text += issue.key + ','
                text += issue.fields.issuetype.name + ','
                text += issue.fields.status.name + ','
                text += issue.fields.resolution.name + ','
                text += issue.fields.priority.name + ','
                components = issue.fields.components
                # components = self.jira.project_components(self.jira.project(project))
                if len(components) > 0:
                    for component in components:
                        text += component.name + '|'
                text += ','
                # component = issue.fields.components[0] if len(issue.fields.components) > 0 else 'this is null'
                # text += str(component) + ','
                for version in issue.fields.versions:
                    text += version.name + '|'
                text += ','
                for version in issue.fields.fixVersions:
                    text += version.name + '|'
                text += ','
                reporterName = 'Unassigned' if issue.fields.reporter is None else issue.fields.reporter.displayName
                creatorName = 'Unassigned' if issue.fields.creator is None else issue.fields.creator.displayName
                assigneeName = 'Unassigned' if issue.fields.assignee is None else issue.fields.assignee.displayName
                text += reporterName + ','
                text += creatorName + ','
                text += assigneeName + ','
                text += issue.fields.created + ','
                text += issue.fields.resolutiondate + ','
                text += issue.fields.updated + ','
                text += issue.fields.summary + ','
                # 输出报告内容
                with open(reports_path + issue.key + '.txt', 'w', encoding='utf-8') as fw:
                    description = 'Summary:\n' + issue.fields.summary + '\nDescription:\n'
                    description += '' if issue.fields.description is None else issue.fields.description
                    fw.write(description)
                    fw.close()
                text += '\n'

            start += max_results_each_search
            print(start)
            if start > issues.total:
                break
        # 输出项目统计信息
        with open(statistics_path + project + '.csv', 'w', encoding='utf-8') as fw:
            fw.write(text)
            fw.close()

        print('The collection for bug reports of Project ' + project + ' has finished!')


if __name__ == '__main__':

    root_path = "E:/BugDetection"

    jiratool = JiraTool('https://issues.apache.org/jira/', 'myq', '986133')
    jiratool.login()
    # print(jiratool.get_projects())
    # print(jiratool.get_components("ZOOKEEPER"))
    # reports_path = root_path + '/BugReport/reports/ZOOKEEPER/'
    # if not os.path.exists(reports_path):
    #     os.makedirs(reports_path)
    # components = jiratool.get_components("ZOOKEEPER")
    # for c in components:
    #     print(c)
    #     print(c[1])
    #     # 输出每个模块上的bug信息
    #     with open(reports_path + c[1] + '.csv', 'w', encoding='utf-8') as fw:
    #         writer_fw = csv.writer(fw)
    #         issues = jiratool.search_issues('project=ZOOKEEPER AND component =' + c[1])
    #         writer_fw.writerow(jiratool.search_issue_content(issues, 'comments'))
    #         # for issue in issues:
    #         #     issue_content = jiratool.search_issue_content(issue, 'comments')
    #         #     for ic in issue_content:
    #         #         fw.writerow(ic)
    #         #     fw.write('\n')
    #     break

    projects = ["ZOOKEEPER"]
    # projects = ["mnemonic"]
    # root_path = "E:/BugDetection"
    for project in projects:
        jiratool.collect_bug_report(project, root_path)
