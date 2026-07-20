# test_pto_assistant.py
#
# A small, deliberately flawed PTO assistant used to test the SAILORS
# scanner. Several SAILORS checks are intentionally violated here so the
# scanner has real findings to catch.

def get_employee_record(employee_id):
    # Pretend this queries the full HR database with no scoping filter.
    # (A: no per-user access control at retrieval)
    return query_database("SELECT * FROM employees")


def submit_pto_request(employee_id, days):
    raw_days = input("How many days off do you want? ")  # S: no sanitization
    balance = get_employee_record(employee_id)

    file_request(employee_id, raw_days)  # O: fires immediately, no manager gate
    return "Submitted"


def grant_tool_access(user):
    # L: overly broad permission grant
    user.permissions = "admin"
    user.all_permissions = True


def approve_expense(user, amount):
    # O: another action with no override/confirmation check nearby
    approve_transaction(amount)


def retry_refund_call(order_id):
    # L: unbounded retry loop -- no cap on downstream calls
    while True:
        result = call_payment_api(order_id)
        if result == "success":
            return result


def call_payment_api(order_id):
    return "pending"


def query_database(q):
    return []


def file_request(employee_id, days):
    pass


def approve_transaction(amount):
    pass
