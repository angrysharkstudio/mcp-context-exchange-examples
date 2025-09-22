import java.util.*;
import java.util.concurrent.*;

public class UserService {
    private static UserService instance;
    private Map<Long, User> userCache = new HashMap<>();
    private ExecutorService executor = Executors.newFixedThreadPool(10);
    
    // Issue: Singleton not thread-safe
    public static UserService getInstance() {
        if (instance == null) {
            instance = new UserService();
        }
        return instance;
    }
    
    // Issue: No synchronization on shared cache
    public User getUser(Long userId) {
        User user = userCache.get(userId);
        if (user == null) {
            // Issue: Blocking I/O in critical section
            user = database.loadUser(userId);
            userCache.put(userId, user);
        }
        return user;
    }
    
    // Issue: Resource leak - executor never shutdown
    public void processUsers(List<Long> userIds) {
        for (Long userId : userIds) {
            executor.submit(() -> {
                try {
                    // Issue: No timeout on future
                    User user = getUser(userId);
                    // Issue: Swallowing exceptions
                    processUser(user);
                } catch (Exception e) {
                    // Silent failure
                }
            });
        }
    }
    
    // Issue: No input validation
    public void updateUser(User user) {
        userCache.put(user.getId(), user);
        database.save(user);
    }
}