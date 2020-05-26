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

    public float walkSpeed = 3f;

    public bool isAllowedToMove = true;

    void Start()
    {
        isAllowedToMove = true;
    }

	void Update () { 

        if(!isMoving && isAllowedToMove)
        {
            input = new Vector2(Input.GetAxis("Horizontal"), Input.GetAxis("Vertical"));
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
            }

        }

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
