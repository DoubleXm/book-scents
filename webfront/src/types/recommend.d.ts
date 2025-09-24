declare namespace Recommend {
  interface RecommendRes {
    id: string;
    content: string;
    rating: number;
    createdTime: string;
    user: User.UserRes;
  }

  type CreateRecommendReq = Pick<RecommendRes, 'content' | 'rating'>;

  type CreateRecommendRes = Pick<RecommendRes, 'id' | 'content' | 'rating' | 'createdTime'>;
}