using UnityEngine;
using System.Collections.Generic;

public class PlayerController : MonoBehaviour 
{
    public float moveSpeed = 5f;
    private List<GameObject> enemies;
    private Transform playerTransform;
    
    void Start() 
    {
        playerTransform = transform;
    }
    
    void Update() 
    {
        // Issue: FindGameObjectsWithTag called every frame
        enemies = new List<GameObject>(GameObject.FindGameObjectsWithTag("Enemy"));
        
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        
        Vector3 movement = new Vector3(horizontal, 0, vertical);
        transform.position += movement * moveSpeed * Time.deltaTime;
        
        // Issue: Inefficient distance checks
        foreach (var enemy in enemies)
        {
            float distance = Vector3.Distance(transform.position, enemy.transform.position);
            if (distance < 10f)
            {
                // Issue: GetComponent called in loop
                enemy.GetComponent<Renderer>().material.color = Color.red;
            }
        }
    }
}