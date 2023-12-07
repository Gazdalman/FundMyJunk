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

export const createProject = (data) => async dispatch => {
  const res = await fetch("/api/projects/new", {
    method: "POST",
    body: data
  })

  const resJson = await res.json()
  if (res.ok) {
    return resJson
  }

  console.log("res errors", resJson);
}

export const createStory = (story, projectId) => async dispatch => {
  const res = await fetch(`/api/projects/${projectId}/story`, {
    method: "POST",
    body: story
  })

  if (res.ok) {
    return "ok"
  }

  const err = await res.json()
  return err
}

export const createReward = (reward, items, projectId) => async dispatch => {
  const res = await fetch(`/api/projects/${projectId}/rewards/new`, {
    method: "POST",
    body: reward
  })
  let broken
  const err = await res.json()
  if (res.ok) {
    // console.log(err.id);
    const id = err.id
    items.forEach(async (item) => {
      const itemRes = await fetch(`/api/rewards/${err.id}/items/new`, {
        method: "POST",
        body: item
      })

      const newItem = await itemRes.json()
      if (itemRes.ok) {
        broken = false
        return broken
      }

      return newItem
    })
  }

  return err
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

export const editStory = (story, storyId) => async dispatch => {
  const res = await fetch(`/api/stories/${storyId}/edit`, {
    method: "PUT",
    body: story
  })

  if (res.ok) {
    return "okay"
  }
  const err = await res.json()
  return err
}

const projects = (state = {}, action) => {
  switch (action.type) {
    case GET_PROJECTS:
      return { ...action.projects }

    default:
      return state;
  }
}

export default projects
