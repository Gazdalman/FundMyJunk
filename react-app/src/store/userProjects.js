const GET_USER_PROJECTS = "userProjects/GET_USER_PROJECTS";
const SET_REQUESTED_PROJECT = "userProjects/SET_REQUESTED_PROJECT";

const setProjects = (projects) => {
  return {
    type: GET_USER_PROJECTS,
    projects
  }
}

const requestedProject = (project) => {
  return {
    type: SET_REQUESTED_PROJECT,
    project
  }
}

export const setRequestedProject = (id) => async dispatch => {
  const res = await fetch(`/api/projects/${id}`)

  const project = await res.json()
  if (res.ok) {
    dispatch(requestedProject(project))
    return project
  }
}

export const getUserProjects = (userId) => async dispatch => {
  const res = await fetch(`/api/projects/users/${userId}`)

  const projects = await res.json()

  if (res.ok) {
    dispatch(setProjects(projects))
  }
}

const userProjects = (state = {}, action) => {
  switch (action.type) {
    case GET_USER_PROJECTS:
      return {...action.projects}
    case SET_REQUESTED_PROJECT:
      return {...action.project}
    default:
      return state
  }
}

export default userProjects