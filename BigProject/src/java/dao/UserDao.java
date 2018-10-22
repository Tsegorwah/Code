package dao;

public interface UserDao {

	public boolean regUser(String username,String password,String sex);

	public boolean checkUser(String username);
	
	public String login(String username,String password);
	
	public boolean changeUser(String username,String password ,String id);
	
	public boolean deleteUser(String id);
}
