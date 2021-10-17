package main;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Map;
import java.util.Objects;

public class Main {

    private static String RESOURCE_PATH;
    private static Index index;

    public static void main(String[] args) throws IOException {
        try {
            RESOURCE_PATH = Objects.requireNonNull(Main.class.getResource("")).getPath() + "/resources/";
            ArrayList<TokenDoc> tokenArr = preprocess(RESOURCE_PATH + "Trec_microblog11.txt");  // preprocessing

            index = new Index(tokenArr);  // indexing
            System.out.println(index.getWeight("dinner", "34952194402811904"));
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

    public static ArrayList<String> getQuery(String fileName) throws IOException {
        File file = new File(fileName);
        ArrayList<String> query = new ArrayList<>();
        BufferedReader in = new BufferedReader(new FileReader(file));
        String line;
        while ((line = in.readLine()) != null) {
            line = line.trim();
            if (line.startsWith("<title>")) {
                query.add(line.substring(7, line.indexOf("</title>")).trim());
            }
        }
        return query;
    }

    public static ArrayList<Similar> Similar(ArrayList<String> query, Index index) {
        ArrayList<String> temp = new ArrayList<>();
        ArrayList<String> fin = new ArrayList<>();
        for (String value : query) {
            for (Map.Entry<String, Double> entry : index.getPosting(value)) {
                temp.add(entry.getKey());
            }
        }
        Collections.sort(temp);
        fin.add(temp.get(0));
        for (int k = 1; k < temp.size(); k++) {
            if (!Objects.equals(temp.get(k), temp.get(k - 1))) {
                fin.add(temp.get(k));
            }
        }
        ArrayList<Similar> similar = new ArrayList<>();

        double[] doctf = new double[query.size()];
        double[] querytf = getQTf(query);
        for (String s : fin) {
            doctf = getDTf(query, doctf, s);
            double similarity = calcSimilarity(querytf, doctf);
            similar.add(new Similar(similarity, s));
        }
        similar.sort(Collections.reverseOrder());
        return similar;
    }

    public static double[] getQTf(ArrayList<String> query) {
        int[] temp = new int[query.size()];
        int counter = 0;
        for (int i = 0; i < query.size(); i++) {
            int index = query.indexOf(query.get(i));
            temp[index]++;
            if (index == i) {
                counter++;
            }
        }
        double[] querytf = new double[counter];
        counter = 0;
        for (int i : temp) {
            if (i != 0) {
                querytf[counter] = i;
                counter++;
            }
        }
        return querytf;
    }

    public static double[] getDTf(ArrayList<String> query, double[] doctf, String docID) {
        for (int i = 0; i < doctf.length; i++) {
            doctf[i] = index.getTF(query.get(i), docID);
        }
        return doctf;
    }

    public static double calcSimilarity(double[] querytf, double[] doctf) {
        double dotProduct = 0.0;
        double normA = 0.0;
        double normB = 0.0;
        for (int i = 0; i < querytf.length; i++) {
            dotProduct += querytf[i] * doctf[i];
            normA += Math.pow(querytf[i], 2);
            normB += Math.pow(querytf[i], 2);
        }
        return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
    }
}
