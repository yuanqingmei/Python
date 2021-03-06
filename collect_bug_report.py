# -*-coding:utf-8-*-
# The script has been tested successfully.

import os
from jira.client import JIRA


def collect(project, root_path):
    jira = JIRA(server="https://issues.apache.org/jira/")

    statistics_path = root_path + '/BugReport/statistics/'
    reports_path = root_path + '/BugReport/reports/' + project + '/'
    if not os.path.exists(statistics_path):
        os.makedirs(statistics_path)
    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    text = 'id, Key, Type, Status, Resolution, Priority, AffectsVersions, FixedVersions, Reporter, Creator,' \
           ' Assignee, CreatedDate, ResolutionDate, UpdatedDate, Summary\n'
    search_str = 'project = ' + project.upper() + ' AND issuetype = Bug AND status in (Resolved, Closed) AND ' \
                                                  'resolution in (Fixed, Resolved) ORDER BY key ASC'

    start = 0
    max_results_each_search = 1000
    while True:
        issues = jira.search_issues(search_str, startAt=start, maxResults=max_results_each_search)
        # print("the issues is ", issues)
        # for issue in issues:
        #     print(issue.fields.summary)
        for issue in issues:
            text += issue.id + ','
            text += issue.key + ','
            text += issue.fields.issuetype.name + ','
            text += issue.fields.status.name + ','
            text += issue.fields.resolution.name + ','
            text += issue.fields.priority.name + ','
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
        if start > issues.total:
            break
    # 输出项目统计信息
    with open(statistics_path + project + '.csv', 'w', encoding='utf-8') as fw:
        fw.write(text)
        fw.close()

    print('The collection for bug reports of Project ' + project + ' has finished!')


if __name__ == '__main__':
    projects = ["accumulo", "activemq", "any23", "camel", "flink", "gora", "ivy", "kafka", "kylin", "lens", "mnemonic",
                "nutch", "storm", "tika", "zeppelin", "zookeeper"]
    projects = ["mnemonic"]
    root_path = "E:/BugDetection"
    for project in projects:
        collect(project, root_path)
