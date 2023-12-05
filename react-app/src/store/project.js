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

export const createProject = (project) => async dispatch => {
  const res = await fetch("/api/projects/new", {
    method: "POST",
    body: project
  })

  if (res.ok) {
    console.log("was okay");
    const project = await res.json()
    return project
  }

  const errs = await res.json()
  console.log("res errors", errs);
}

export const editProject = (project, id) => async dispatch => {
  const res = await fetch(`/api/projects/${id}/edit`, {
    method: "PUT",
    body: project
  })

  const editedProject = await res.json()

  if (res.ok) {
    return editedProject
  }

  return editedProject
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
