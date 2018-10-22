package bean;

public class Topic {
	private int id;
	private String username;
	private String title;
    private String topicdate;
    private String content;
    private int replycount;
	
    public Topic() {
		super();
		// TODO Auto-generated constructor stub
	}

	public Topic(int id, String username, String title, String topicdate, String content, int replycount) {
		super();
		this.id = id;
		this.username = username;
		this.title = title;
		this.topicdate = topicdate;
		this.content = content;
		this.replycount = replycount;
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

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getTopicdate() {
		return topicdate;
	}

	public void setTopicdate(String topicdate) {
		this.topicdate = topicdate;
	}

	public String getContent() {
		return content;
	}

	public void setContent(String content) {
		this.content = content;
	}

	public int getReplycount() {
		return replycount;
	}

	public void setReplycount(int replycount) {
		this.replycount = replycount;
	}

	
    
    
}
