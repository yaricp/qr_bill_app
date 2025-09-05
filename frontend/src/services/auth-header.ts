export default function authHeader() {
  let user;
  let local_db_user = localStorage.getItem('user');
  if (local_db_user){
    user = JSON.parse(local_db_user);
  }
  if (user && user.accessToken) {
    return { Authorization: 'Bearer ' + user.accessToken };
  } else {
    return {};
  }
}