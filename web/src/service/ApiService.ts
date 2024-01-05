import http from "./httpclient";

class ApiService {
  signin(email: string, password: string) {
    return http.post(
      `/api/signin`,
      {
        email: `${email}`,
        password: `${password}`
      }
    );
  }

  signup(userName: string, email: string, password: string) {
    return http.post(
      `/api/signup`,
      {
        userName: `${userName}`,
        email: `${email}`,
        password: `${password}`
      }
    );
  }

  getProfile(myUserId: number, userId: number) {
    return http.post(
      `/api/profile`,
      {
        myUserId: `${myUserId}`,
        userId: `${userId}`
      }
    );
  }
  updateProfile(userId: number, content: string, formContent: string, password: string) {
    return http.post(
      `/api/update_profile/${content}`,
      {
        userId: `${userId}`,
        formContent: `${formContent}`,
        password: `${password}`
      }
    );
  }
  newThread(threadName: string, text: string, userId: number) {
    return http.post(
      `/api/new_thread`,
      {
        threadName: `${threadName}`,
        text: `${text}`,
        userId: `${userId}`
      }
    );
  }

  getThreadList(threadName: string) {
    return http.get(`/api/search?threadname=${threadName}`)
  }

  getThread(threadId: number) {
    return http.get(`/api/thread/${threadId}`)
  }

  postContent(text: string, threadId: number, user_id: number) {
    return http.post(
      `/api/thread/${threadId}`,
      {
        text: `${text}`,
        user_id: `${user_id}`
      }
    );
  }
  postContentWithFile(file: File,text: string, threadId: number, user_id: number) {
    const form = new FormData()
    form.append('file',file)
    return http.post(
      `/api/threadWithFile/${threadId}?text=${text}&user_id=${user_id}`,
      form,
      {
        headers: {
          'content-type': 'multipart/form-data'
        },
      }
    );
  }
}


export default new ApiService();
