import { axios } from '@/utils/http';

export const login = (data: User.UserLoginReq) => {
  return axios.post<User.UserLoginOfRegisterRes>('/login', data);
}

export const register = (data: User.UserRegisterReq) => {
  return axios.post<User.UserLoginOfRegisterRes>('/register', data);
}

export const getUser = () => {
  return axios.get<User.UserRes>('/user');
}

export const fetchBooks = (params: Partial<Book.BooksReq>) => {
  return axios.get<ListResult<Book.BooksRes>>('/books', { params });
}

export const createBook = (data: Book.CreateBookReq) => {
  return axios.post('/books', data, { headers: {'Content-Type': 'multipart/form-data'} });
}

export const fetchBookById = (id: string) => {
  return axios.get<Book.BookDetailRes>(`/books/${id}`);
}

export const createBookRead = (id: string) => {
  return axios.patch<Book.BookDetailRes>(`/books/${id}/read`);
}

export const fetchRecommends = (id: string) => {
  return axios.get<ListResult<Recommend.RecommendRes>>(`/comments/${id}`);
}

export const createRecommend = (id: string, data: Recommend.CreateRecommendReq) => {
  return axios.post<Recommend.CreateRecommendRes>(`/comments/${id}`, data);
}
