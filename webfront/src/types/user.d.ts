declare namespace User {
  interface UserLoginReq {
    username: string;
    password: string;
  }

  interface UserRegisterReq extends UserLoginReq {
    mobile: string;
  }

  interface UserRes {
    id: string;
    name: string;
    cover: string;
    mobile: string;
  }

  interface UserLoginOfRegisterRes {
    profile: UserRes;
    token: string;
  }
}