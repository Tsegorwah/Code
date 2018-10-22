package bean;

public class User {
	private int id;
	private String username;
	private String password;
    private String sex;
    
	public User() {
		super();
		// TODO Auto-generated constructor stub
	}

	public User(int id, String password, String username, String sex) {
		super();
		this.id = id;
		this.username = username;
		this.password = password;
		this.sex = sex;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getUsername() {
		return username;
	}

	public void setUsername(String username) {
		this.username = username;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}

	public String getSex() {
		return sex;
	}

	public void setSex(String sex) {
		this.sex = sex;
	}

	
}
