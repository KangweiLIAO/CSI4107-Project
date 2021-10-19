package main;

import java.util.ArrayList;

public class Query {
    public String qid = "-1";
    public ArrayList<String> queryTerms;

    // Default Constructor
    public Query() {
    }

    // Constructor
    public Query(String qid, ArrayList<String> queryTerms) {
        this.qid = qid;
        this.queryTerms = queryTerms;
    }

    public void setQid(String id) {
        this.qid = id;
    }

    public String getQid() {
        return qid;
    }

    public void setQueryTerms(ArrayList<String> queryTerms) {
        this.queryTerms = queryTerms;
    }

    public ArrayList<String> getQueryTerms() {
        return queryTerms;
    }
}
