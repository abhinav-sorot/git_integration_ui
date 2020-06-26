from home_page import HomePage
from login_page import Login


def test_create_git_repo():
    try:
        login = Login()
        home = HomePage()
        username = input("enter git username: ")
        password = input("enter git password: ")
        repo_name = input("enter repo name to create: ")
        issue_name = input("enter issue name to create: ")
        comments = input("please provide comments: ")
        login.perform_login(username, password)
        repo_full_name = home.create_repository(repo_name)
        issue_number = home.create_issue(issue_name)
        home.comment_and_add_emoji(comments)
        assert home.link_issue_via_comment(issue_number)
        assert not home.delete_repo(repo_full_name)
    except Exception as e:
        print(e)
        assert False
