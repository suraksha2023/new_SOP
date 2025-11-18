import time
import pytest
from utilities.data_access import read_sop_data
from pages.login_page import LoginPage
from pages.sop_proposer_page import SOPProposerPage
from pages.sop_recommender_page import SOPRecommenderPage
from pages.sop_approver_page import SOPApproverPage
from pages.sop_proposer_verapproval import SOPProposerApproval
from pages.sop_published import SOPPublishPage

# Load Excel data once
sop_data = read_sop_data("data/sop_data.xlsx")

approver_roles = [f"Approver{i}" for i in range(1, 8)]  # For Approver1 to Approver7

@pytest.mark.parametrize("data", sop_data)
def test_sop_full_flow_ddt(driver, data):
    login = LoginPage(driver)
    proposer = SOPProposerPage(driver)
    recommender = SOPRecommenderPage(driver)
    approver = SOPApproverPage(driver)
    proposer_approval = SOPProposerApproval(driver)
    publisher = SOPPublishPage(driver)

    role = data["role"]
    username = data["username"]
    password = data["password"]
    sop_title = data["sop_title"]
    sop_file = data.get("file_path")

    print(f"\n🔹 Running step for {role} ({username})")

    login.login(username, password)
    if role == "Proposer":
        proposer.create_new_document(sop_title, sop_file)
    elif role == "Recommender":
        recommender.find_document_across_pages(sop_title)
    elif role in approver_roles:
        approver.open_and_approve_from_last_page(sop_title)
    elif role == "Proposer_Verification":
        proposer_approval.open_and_approve(sop_title)
    elif role == "Publisher":
        publisher.open_and_approve(sop_title)
    else:
        pytest.skip(f"⚠️ Unknown role type: {role}")
    login.logout()
    time.sleep(3)

