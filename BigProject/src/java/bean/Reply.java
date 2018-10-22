package bean;

public class Reply {
	private int id;
	private String username;
    private String replyDate;
    private int replycontent;
	
    public Reply() {
		super();
		// TODO Auto-generated constructor stub
	}

	public Reply(int id, String username, String replyDate, int replycontent) {
		super();
		this.id = id;
		this.username = username;
		this.replyDate = replyDate;
		this.replycontent = replycontent;
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

	public String getReplyDate() {
		return replyDate;
	}

	public void setReplyDate(String replyDate) {
		this.replyDate = replyDate;
	}

	public int getReplycontent() {
		return replycontent;
	}

	public void setReplycontent(int replycontent) {
		this.replycontent = replycontent;
	}
	
    
}
