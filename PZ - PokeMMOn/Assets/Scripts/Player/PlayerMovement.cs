using UnityEngine;
using System.Collections;

enum Direction
{
    North,
    East,
    South,
    West
}

public class PlayerMovement : MonoBehaviour {

    Direction currentDirection;
    Vector2 input;
    bool isMoving = false;
    Vector3 startPos;
    Vector3 endPos;
    float time;

    public Sprite northSprite;
    public Sprite eastSprite;
    public Sprite southSprite;
    public Sprite westSprite;

    public float walkSpeed;
    private Rigidbody2D myRigidbody;
    private Vector3 change;

    public bool isAllowedToMove = true;

    public Animator animator;

    

    void Start()
    {
        isAllowedToMove = true;
        myRigidbody = GetComponent<Rigidbody2D>();
    }

	void Update () {

        change = Vector3.zero;
        if(!isMoving && isAllowedToMove)
        {
            change.x = Input.GetAxisRaw("Horizontal");
            change.y = Input.GetAxisRaw("Vertical");
            if (change != Vector3.zero)
            {
                if (change.x < 0)
                {
                    //animator.SetInteger("Face", 2);
                    currentDirection = Direction.West;
                    animator.SetInteger("Face", 6);
                }
                if (change.x > 0)
                {
                    // animator.SetInteger("Face", 4);

                    currentDirection = Direction.East;
                    animator.SetInteger("Face", 8);
                }
                if (change.y < 0)
                {
                    //animator.SetInteger("Face", 3);
                    currentDirection = Direction.South;
                    animator.SetInteger("Face", 7);
                }
                if (change.y > 0)
                {
                    //animator.SetInteger("Face", 1);
                    currentDirection = Direction.North;
                    animator.SetInteger("Face", 5);
                }
               
                MoveCharacter();

                

                switch (currentDirection)
                {
                    case Direction.North:
                        animator.SetInteger("Face", 1);
                       
                       // gameObject.GetComponent<SpriteRenderer>().sprite = northSprite;
                        
                        break;
                    case Direction.East:
                        animator.SetInteger("Face", 4);
                       // gameObject.GetComponent<SpriteRenderer>().sprite = eastSprite;
                        break;
                    case Direction.South:
                        animator.SetInteger("Face", 3);
                        //gameObject.GetComponent<SpriteRenderer>().sprite = southSprite;
                        break;
                    case Direction.West:
                        animator.SetInteger("Face", 2);
                       // gameObject.GetComponent<SpriteRenderer>().sprite = westSprite;
                        break;
                }
            }


                /*input = new Vector2(Input.GetAxisRaw("Horizontal"), Input.GetAxisRaw("Vertical"));
            if (Mathf.Abs(input.x) > Mathf.Abs(input.y))
                input.y = 0;
            else
                input.x = 0;

            if(input != Vector2.zero)
            {

                if(input.x < 0)
                {
                    currentDirection = Direction.West;
                }
                if(input.x > 0)
                {
                    currentDirection = Direction.East;
                }
                if(input.y < 0)
                {
                    currentDirection = Direction.South;
                }
                if (input.y > 0)
                {
                    currentDirection = Direction.North;
                }

                switch(currentDirection)
                {
                    case Direction.North:
                        gameObject.GetComponent<SpriteRenderer>().sprite = northSprite;
                        break;
                    case Direction.East:
                        gameObject.GetComponent<SpriteRenderer>().sprite = eastSprite;
                        break;
                    case Direction.South:
                        gameObject.GetComponent<SpriteRenderer>().sprite = southSprite;
                        break;
                    case Direction.West:
                        gameObject.GetComponent<SpriteRenderer>().sprite = westSprite;
                        break;
                }

                StartCoroutine(Move(transform));
            }*/

        }

	}

    void MoveCharacter()
    {
        myRigidbody.MovePosition(transform.position + change * walkSpeed * Time.deltaTime);
    }

    public IEnumerator Move(Transform entity)
    {
        isMoving = true;
        startPos = entity.position;
        time = 0;

        endPos = new Vector3(startPos.x + System.Math.Sign(input.x), startPos.y + System.Math.Sign(input.y), startPos.z);

        while (time < 1f)
        {
            time += Time.deltaTime * walkSpeed;
            entity.position = Vector3.Lerp(startPos, endPos, time);
            yield return null;
        }

        isMoving = false;
        yield return 0;
    }
}
