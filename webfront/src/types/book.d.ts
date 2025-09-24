declare namespace Book {

  interface BooksReq {
    pageSize: number;
    pageNum: number;
    name: string;
    order: 'DESC' | 'ASC';
    filed: 'HOT' | 'RECOMMEND';
  }

  interface BooksRes {
    id: string;
    name: string;
    url: string;
    description: string;
    cover: string;
    author: string;
    publisher: string;
    publisherDate: string;
    hot: number;
    recommend: number;
    createdTime: string;
    updatedTime: string;
  }

  interface BookDetailRes extends Pick<BooksRes, 'id' | 'name' | 'cover' | 'description' | 'author' | 'url'> {
    rating: number;
    statement: number[];
  }

  interface CreateBookReq extends Pick<BooksRes, 'name' | 'author' | 'description'> {
    cover: File | null;
  }
}