import com.google.api.client.auth.oauth2.Credential;
import com.google.api.client.extensions.java6.auth.oauth2.AuthorizationCodeInstalledApp;
import com.google.api.client.extensions.jetty.auth.oauth2.LocalServerReceiver;
import com.google.api.client.googleapis.auth.oauth2.GoogleAuthorizationCodeFlow;
import com.google.api.client.googleapis.auth.oauth2.GoogleClientSecrets;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.util.store.FileDataStoreFactory;
import com.google.api.client.util.DateTime;

import com.google.api.services.calendar.CalendarScopes;
import com.google.api.services.calendar.model.*;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.List;
import java.util.HashMap;
import java.io.FileReader;
import java.util.Iterator;
import java.lang.StringBuilder;
import java.io.BufferedReader;

public class EventsMaker{
    /** Application name. */
    private static final String APPLICATION_NAME =
        "Google Calendar API Java Quickstart";

    /** Directory to store user credentials for this application. */
    private static final java.io.File DATA_STORE_DIR = new java.io.File(
        System.getProperty("user.home"), ".credentials/events-maker");

    /** Global instance of the {@link FileDataStoreFactory}. */
    private static FileDataStoreFactory DATA_STORE_FACTORY;

    /** Global instance of the JSON factory. */
    private static final JsonFactory JSON_FACTORY =
        JacksonFactory.getDefaultInstance();

    /** Global instance of the HTTP transport. */
    private static HttpTransport HTTP_TRANSPORT;

    //Keys from json file and hash table
    private static final String KEY_MESSAGE="message";
    private static final String KEY_ID="id";
    private static final String KEY_DATE="appDate";
    private static final String KEY_TIME="appTime";
    private static final String KEY_OFFSET="offset";
    private static final String KEY_FULLTIME="fulltime";

    /** Global instance of the scopes required by this quickstart.
     *
     * If modifying these scopes, delete your previously saved credentials
     * at ~/.credentials/calendar-java-quickstart
     */
    private static final List<String> SCOPES =
        Arrays.asList(CalendarScopes.CALENDAR);

    static {
        try {
            HTTP_TRANSPORT = GoogleNetHttpTransport.newTrustedTransport();
            DATA_STORE_FACTORY = new FileDataStoreFactory(DATA_STORE_DIR);
        } catch (Throwable t) {
            t.printStackTrace();
            System.exit(1);
        }
    }

    /**
     * Creates an authorized Credential object.
     * @return an authorized Credential object.
     * @throws IOException
     */
    public static Credential authorize() throws IOException {
        // Load client secrets.
        InputStream in =
            EventsMaker.class.getResourceAsStream("/client_secret.json");
        GoogleClientSecrets clientSecrets =
            GoogleClientSecrets.load(JSON_FACTORY, new InputStreamReader(in));

        // Build flow and trigger user authorization request.
        GoogleAuthorizationCodeFlow flow =
                new GoogleAuthorizationCodeFlow.Builder(
                        HTTP_TRANSPORT, JSON_FACTORY, clientSecrets, SCOPES)
                .setDataStoreFactory(DATA_STORE_FACTORY)
                .setAccessType("offline")
                .build();
        Credential credential = new AuthorizationCodeInstalledApp(
            flow, new LocalServerReceiver()).authorize("user");
        System.out.println(
                "Credentials saved to " + DATA_STORE_DIR.getAbsolutePath());
        return credential;
    }

    /**
     * Build and return an authorized Calendar client service.
     * @return an authorized Calendar client service
     * @throws IOException
     */
    public static com.google.api.services.calendar.Calendar
        getCalendarService() throws IOException {
        Credential credential = authorize();
        return new com.google.api.services.calendar.Calendar.Builder(
                HTTP_TRANSPORT, JSON_FACTORY, credential)
                .setApplicationName(APPLICATION_NAME)
                .build();
    }

    private static void setKeyValue(String key,
            HashMap<String,String> mapper,
            JSONObject jsonObject) {
        if (jsonObject.get(key)!=null) {
            mapper.put(key,(String)jsonObject.get(key));
        }
    }

    //Get Json file
    private static HashMap<String,String> getJson(String path) 
        throws IOException{
        JSONParser parser = new JSONParser();
        HashMap<String,String> mapper=new HashMap<String,String>();
        //Set default value
        mapper.put(KEY_MESSAGE,"Praise The Sun");
        mapper.put(KEY_ID,"antimonitor02@gmail.com");
        mapper.put(KEY_DATE,"2017-04-15");
        mapper.put(KEY_TIME,"14:00:00");
        mapper.put(KEY_OFFSET,"-07:00");

        try {
            InputStream in =
                EventsMaker.class.getResourceAsStream("/event.json");
            BufferedReader br = new BufferedReader(new InputStreamReader(in, "UTF-8"));
            Object obj = parser.parse(br);
            JSONObject jsonObject = (JSONObject) obj;
            setKeyValue(KEY_MESSAGE,mapper,jsonObject);
            setKeyValue(KEY_ID,mapper,jsonObject);
            setKeyValue(KEY_DATE,mapper,jsonObject);
            setKeyValue(KEY_TIME,mapper,jsonObject);
            String fullDateTime=mapper.get(KEY_DATE)+"T"+
                mapper.get(KEY_TIME)+
                mapper.get(KEY_OFFSET);
            mapper.put(KEY_FULLTIME,fullDateTime);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return mapper;
    }

    public static void main(String[] args) throws IOException {
        // Build a new authorized API client service.
        // Note: Do not confuse this class with the
        //   com.google.api.services.calendar.model.Calendar class.
        com.google.api.services.calendar.Calendar service =
            getCalendarService();

        //This file is at java/src/main/resources
        HashMap<String,String> data=getJson("event.json");

        Event event = new Event()
                .setSummary(data.get(KEY_MESSAGE));
        System.out.println(data.get(KEY_MESSAGE));
        DateTime startDateTime = new DateTime(data.get(KEY_FULLTIME));
        EventDateTime start = new EventDateTime()
                .setDateTime(startDateTime)
                    .setTimeZone("America/New_York");
        event.setStart(start);
        event.setEnd(start);

        /*
        String[] recurrence = new String[] {"RRULE:FREQ=DAILY;COUNT=2"};
        event.setRecurrence(Arrays.asList(recurrence));

        EventAttendee[] attendees = new EventAttendee[] {
                new EventAttendee().setEmail("thanos.trn11@outlook.com"),
                        new EventAttendee().setEmail("thanos.trn11@gmail.com"),
        };
        event.setAttendees(Arrays.asList(attendees));

        EventReminder[] reminderOverrides = new EventReminder[] {
                new EventReminder().setMethod("email").setMinutes(24 * 60),
                        new EventReminder().setMethod("popup").setMinutes(10),
        };

        Event.Reminders reminders = new Event.Reminders()
                .setUseDefault(false)
                    .setOverrides(Arrays.asList(reminderOverrides));
        event.setReminders(reminders);
        */

        //////////////////////////////////////////////////////////////////////////////////////
        //
        //
        //NOTE: Use your own gmail address to post event to your calendar
        //To set gmail name: go to src/main/resources/event.json and edit the id key's value
        //
        //
        //////////////////////////////////////////////////////////////////////////////////////
        String calendarId =data.get(KEY_ID);
        event = service.events().insert(calendarId, event).execute();
        System.out.printf("Event created: %s\n", event.getHtmlLink());
    }

}
