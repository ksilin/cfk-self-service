# cfk self-service

A simplified example of self-service for generation of CfK topic resources for a GitOps workflow.

<img src="https://github.com/user-attachments/assets/89bee193-d709-4a39-9864-434fd3802581" alt="Create Topic UI" width="400">

![Screenshot 2024-10-14 at 10 01 44|800](https://github.com/user-attachments/assets/294b91d9-ea07-4ac2-ac9e-69ddcc311ccd)

### UI

Simple form, sending POST requests to the backend.

Preliminary validation happens in the form. 

CD into the `frontend` folder.

Prepare frontend: `npm install`

Run frontend: `npm start`


### Backend

Add configuration - the default filename is `topic_context_config`

Namespace overrides the default namespace
Prefix is prepended to the user-defined topic name
Repository name: where do you want the topic CRs to be placed as PRs
Github token: needs permission to create PRs on the repository

```yaml
namespace: new_topic-namespace
prefix: new-topic-prefix-
repository_name: your-org/topics-for-domain
github_token: github_pat_1234567890
```

CD into the `backend` folder

Install dependencies `pip install -r requirements.txt`

Run backend: `python app.py`

#### Create CR from template

Done in the `app.py` itself

#### Modify CR from config

Performed by the `process_yaml.py`

#### Create PR from modified CR

Performed by the `github_utils.py`
