package main;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Objects;

public class Main {

    private static String RESOURCE_PATH;

    public static void main(String[] args) throws IOException {
        try {
            RESOURCE_PATH = Objects.requireNonNull(Main.class.getResource("")).getPath() + "/resources/";
            ArrayList<TokenDoc> tokenArr = preprocess(RESOURCE_PATH + "Trec_microblog11.txt");  // preprocessing

            Index index = new Index(tokenArr);  // indexing
            System.out.println(index); // Warning - huge to print
        } catch (NullPointerException | IOException err) {
            System.out.println("File not found or Null pointer exception occurred : " + err);
            throw err;
        }
    }

    public static ArrayList<TokenDoc> preprocess(String fileName) throws IOException {
        File file = new File(fileName);
        ArrayList<TokenDoc> TokenDocArray = new ArrayList<>();
        ArrayList<String> stopWords = readStopWord(RESOURCE_PATH + "StopWords.txt");
        BufferedReader in = new BufferedReader(new FileReader(file));
        String line;
        while ((line = in.readLine()) != null) {
            String[] terms = line.split(" ");
            ArrayList<String> list = new ArrayList<>();
            for (String s : terms) {
                s = s.replaceAll("[^0-9a-zA-Z]", ""); // get rid of the symbol in terms
                if (s.equals("") || (s.startsWith("http"))) { // get rid of the space and the web address
                    continue;
                } else {
                    list.add(s);
                }
                // get the documents without stop words
                for (String stopWord : stopWords) {
                    if (s.equals(stopWord)) {
                        list.remove(s);
                        break;
                    }
                }
            }
            String TokenDocID = list.get(0).substring(0, 17); // get an arraylist contains token documents
            list.remove(0); // remove the id from the list
//                System.out.println(TokenDocID);
//                System.out.println(list);
            TokenDoc td = new TokenDoc(TokenDocID, list);
            TokenDocArray.add(td);
        }
        return TokenDocArray;
    }

    public static ArrayList<String> readStopWord(String fileName) throws IOException {
        File file = new File(fileName);
        ArrayList<String> stopWords = new ArrayList<>();
        BufferedReader in = new BufferedReader(new FileReader(file));
        String line;
        while ((line = in.readLine()) != null) {
            stopWords.add(line);
        }
        return stopWords;
    }
}
