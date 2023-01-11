def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assingment_resubmitt_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'

def test_no_headers(client):
    response = client.post(
        '/student/assignments/submit',
        headers=None,
        json={
            'id': 2,
            'teacher_id': 2
        })
    assert response.status_code == 401

def test_submit_assignment_invalid_method(client, h_student_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.get(
        '/student/assignments/submit',
        headers=h_student_1
        , json={
            'id': 2,
            'teacher_id': 2
        }
    )

    assert response.status_code == 405


def test_invalid_headers(client, h_invalid):
    response = client.post(
        '/student/assignments/submit',
        headers=h_invalid,
        json={
            'id': 2,
            'teacher_id': 2
        })
    assert response.status_code == 403
