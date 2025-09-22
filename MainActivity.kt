import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class MainActivity : AppCompatActivity() {
    private var userList: List<User>? = null
    private lateinit var adapter: UserAdapter
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Issue: Network call on main thread
        loadUsers()
        
        // Issue: Potential NPE - adapter not initialized
        recyclerView.adapter = adapter
    }
    
    private fun loadUsers() {
        lifecycleScope.launch {
            // Issue: No error handling
            val response = apiService.getUsers()
            
            // Issue: UI update not on main thread
            userList = response.body()
            
            // Issue: No null check
            adapter.updateData(userList!!)
        }
    }
    
    override fun onResume() {
        super.onResume()
        // Issue: Memory leak - coroutine not cancelled
        lifecycleScope.launch(Dispatchers.IO) {
            while (true) {
                // Polling without lifecycle awareness
                checkForUpdates()
                Thread.sleep(5000)
            }
        }
    }
}