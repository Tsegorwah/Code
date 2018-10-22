package dao;

import java.util.ArrayList;

import bean.Topic;

public interface TopicDao {

	public boolean addTopic(String username,String title,String content);
	
	public ArrayList getTopicByPage(int pageSize,int currentPage);
	
	public int getRowCount();
	
	public int getReplyCount();
	
	public Topic getTopicById(String id);
	
	public ArrayList getHotReplyByPage(int pageSize,int currentPage);
	
	public ArrayList getTopicByUsername(String username);

	public boolean deleteTopic(String id);
}
