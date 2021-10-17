package main;

import java.util.*;

public class Index {

    private final HashMap<String, LinkedList<Map.Entry<String, Double>>> termMap; // HashMap<term, LinkedList<Map.Entry<docID, weight>>>
    private final HashMap<String, Integer> freqMap; // HashMap<term, frequency>

    public Index(ArrayList<TokenDoc> docs) {
        termMap = new HashMap<>();
        freqMap = new HashMap<>();
        for (TokenDoc doc : docs) {
            ArrayList<String> tokens = doc.getTokens(); // get tokens from tokenized document
            for (String token : tokens) {
                Map.Entry<String, Double> tmp = new AbstractMap.SimpleEntry<>(doc.getID(), computeTF(token, doc));
                if (!termExist(token)) {
                    // if token not in index, put the term into the hashmap:
                    termMap.put(token, new LinkedList<>(List.of(tmp)));
                    freqMap.put(token, 1);
                } else {
                    // if token in index, append the docID, tf value to the corresponding term
                    freqMap.replace(token, freqMap.get(token) + 1); // update freqMap for the term
                    termMap.get(token).add(tmp);
                }
            }
        }
    }

    private double computeTF(String token, TokenDoc doc) {
        double nij = 0;
        for (String words : doc.getTokens()) {
            if (words.equalsIgnoreCase(token)) nij++;
        }
        return nij / doc.getTokens().size();
    }

    /**
     * @param term word to test the existence
     * @return true if the term exist in inverted index, false otherwise.
     */
    public boolean termExist(String term) {
        return termMap.getOrDefault(term, null) != null;
    }

    /**
     * @param term  word to get the freq for
     * @param docID specified docID to get weight of
     * @return the weight of the term in specified doc
     * @throws NullPointerException if term not found
     */
    public Double getTF(String term, String docID) throws NullPointerException {
        for (Map.Entry<String, Double> pair : termMap.get(term)) {
            if (pair.getKey().equals(docID)) {
                return pair.getValue();
            }
        }
        throw new NullPointerException("The specified term not found in termMap.");
    }

    public Integer getFreq(String term) throws NullPointerException {
        return freqMap.get(term);
    }

    public LinkedList<Map.Entry<String, Double>> getPosting(String term) throws NullPointerException {
        return termMap.get(term);
    }

    public int length() {
        return termMap.size();
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder();
        for (Map.Entry<String, LinkedList<Map.Entry<String, Double>>> entry : termMap.entrySet()) {
            String term = entry.getKey();
            result.append("{").append(term).append("(").append(freqMap.get(term)).append(") : ");
            for (Map.Entry<String, Double> pair : entry.getValue()) {
                result.append("[").append(pair).append("], ");
            }
            result.append("}");
        }
        return result.toString();
    }
}