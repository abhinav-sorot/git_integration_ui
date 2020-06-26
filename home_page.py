import time

from selenium_wrapper import SeleniumWrapper


class HomePage(SeleniumWrapper):
    link_create_repo = {"css": "#repos-container .btn-primary"}
    txt_repo_name = {"id": "repository_name"}
    btn_create = {"css": ".first-in-line"}

    link_issues = {"css": "[data-selected-links*='repo_issues']"}
    span_new_issue = {"xpath": "//span[text()='New issue']"}
    txt_issue_title = {"id": "issue_title"}
    btn_submit_issue = {"css": "[class='btn btn-primary']"}

    ta_comment = {"id": "new_comment_field"}
    btn_comment = {"css": "[class='bg-gray-light ml-1'] button"}
    svg_emoji = {"css": ".timeline-comment-actions .octicon-smiley"}
    select_emoji = {"css": "[value='THUMBS_UP react']"}

    click_settings = {"css": "[data-ga-click*='Settings']"}
    delete_repository = {"xpath": "//summary[contains(text(), 'Delete this repository')]"}

    repo_owner = {"id": "repository-owner"}
    txt_del_repo_name = {"css": "[aria-label*='delete this repository.']"}
    confirm_delete = {"xpath": "//button[contains(text(),'delete this repository')]"}

    def delete_repo(self, data):
        self.element_click(self.click_settings)
        self.js_click(self.delete_repository)
        self.send_text(data, self.txt_del_repo_name)
        self.js_click(self.confirm_delete)
        only_repo_name = data.split('/')[1]
        check_repo_deleted = {"css": f"#repos-container span[title='{only_repo_name}']"}
        return self.is_element_present(check_repo_deleted, 3)

    def create_repository(self, repo_name):
        self.element_click(self.link_create_repo)
        element_text = self.get_element(self.repo_owner).text
        self.send_text(repo_name, self.txt_repo_name)
        self.element_click(self.btn_create)
        return element_text + "/" + repo_name

    def create_issue(self, issue):
        self.element_click(self.link_issues)
        self.element_click(self.span_new_issue)
        self.send_text(issue, self.txt_issue_title)
        self.element_click(self.btn_submit_issue)
        return self.get_element({"xpath": f"//span[contains(text(),'{issue}')]/following-sibling::span"}).text

    def comment_and_add_emoji(self, comment):
        self.send_text(comment, self.ta_comment)
        self.element_click(self.btn_comment)
        self.element_click(self.svg_emoji)
        self.js_click(self.select_emoji)

    def link_issue_via_comment(self, issue_number):
        time.sleep(2)
        self.send_text(issue_number, self.ta_comment)
        self.element_click(self.btn_comment)
        issue_link = {"xpath": f"//a[text()='{issue_number}']"}
        self.element_click(issue_link)
        return f"issues/{issue_number[1:]}" in self.driver.current_url
