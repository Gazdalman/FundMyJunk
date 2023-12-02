const GET_PROJECTS = "projects/getAll"
const CREATE_PROJECT = "projects/createProject"
const EDIT_PROJECT = "projects/editProject"

const populateProjects = (projects) => {
  return {
    type: GET_PROJECTS,
    projects
  }
}

export const getAllProjects = () => async dispatch => {
  const res = await fetch("/api/projects")

  const projects = await res.json()
  if (res.ok) {
    dispatch(populateProjects(projects))
    return projects
  }
}

const projects = (state = {}, action) => {
  switch (action.type) {
    case GET_PROJECTS:
      return {...action.projects}

    default:
      return state;
  }
}

export default projects
