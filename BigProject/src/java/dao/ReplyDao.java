package dao;

import java.util.ArrayList;

import bean.Reply;

public interface ReplyDao {
	public boolean addReply(String username, String replyContent, int topicId);
	
	public ArrayList getReplyContentByPage(int pageSize,int currentPage,int topicId);
	
	public int getRowCount();
	
	public Reply getReplyById(String id);
}
