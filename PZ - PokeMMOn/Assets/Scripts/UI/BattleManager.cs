using System.Collections;
using System.Collections.Generic;
using Unity.Mathematics;
using UnityEngine;
using UnityEngine.UI;

public class BattleManager : MonoBehaviour
{
    public BattleMenu currentMenu;
    private BattleMenu previousMenu;
    public GameManager gameManager;
    private int infoCounter;
    public Player player;
    public BasePokemon chosenPokemon;
    private bool myTurn;
    private bool wasEnemyTurn;
    private int chosenMove;

    // -1: had no effect, 0: wasn't very effective, 1: normal effect, 2: was super effective
    private int moveWasEffective;

    [Space(10)]
    [Header("Selection")]
    public GameObject selectionMenu;
    public GameObject selectionInfo;
    public Text selectionInfoText;
    public Text fightText;
    private string fightT;
    public Text bagText;
    private string bagT;
    public Text runText;
    private string runT;
    public Text pokemonText;
    private string pokemonT;

    [Space(10)]
    [Header("Moves")]
    public GameObject movesMenu;
    public GameObject movesDetails;
    public Text PP;
    public Text pokemonType;
    public Text moveO;
    private string moveOT;
    public Text moveT;
    private string moveTT;
    public Text moveTH;
    private string moveTHT;
    public Text moveF;
    private string moveFT;

    [Space(10)]
    [Header("Info")]
    public GameObject infoMenu;
    public Text infoText;

    [Space(10)]
    [Header("Misc")]
    public int currentSelection;

    [Space(10)]
    [Header("Misc")]
    public Text enemyPokemonLevel;
    public Text allyPokemonLevel;
    public Text playerHealth;

    // Start is called before the first frame update
    void Start()
    {
        chosenPokemon = player.defaultPokemon;

        gameManager.DisplayPlayerPokemon(chosenPokemon);

        enemyPokemonLevel.text = "Lv" + gameManager.battlePokemon.level.ToString();
        allyPokemonLevel.text = "Lv" + chosenPokemon.level.ToString();

        playerHealth.text = chosenPokemon.HP.ToString() + "/" + chosenPokemon.GetMaxHP().ToString();

        moveO.text = chosenPokemon.moves[0].Name;
        moveT.text = chosenPokemon.moves[1].Name;
        moveTH.text = chosenPokemon.moves[2].Name;
        moveF.text = chosenPokemon.moves[3].Name;

        chosenPokemon.moves[0].currentPP = chosenPokemon.moves[0].pp;
        chosenPokemon.moves[1].currentPP = chosenPokemon.moves[1].pp;
        chosenPokemon.moves[2].currentPP = chosenPokemon.moves[2].pp;
        chosenPokemon.moves[3].currentPP = chosenPokemon.moves[3].pp;

        infoCounter = 0;
        fightT = fightText.text;
        bagT = bagText.text;
        runT = runText.text;
        pokemonT = pokemonText.text;

        moveOT = moveO.text;
        moveTT = moveT.text;
        moveTHT = moveTH.text;
        moveFT = moveF.text;

        // The faster Pokemon starts the turn first
        if(chosenPokemon.pokemonStats.SpeedStat > gameManager.battlePokemon.pokemonStats.SpeedStat)
        {
            myTurn = true;
        }
        else
        {
            myTurn = true;
            // TODO: uncomment when enemy turn works
            //myTurn = false;
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (myTurn)
        {
            if(wasEnemyTurn)
            {
                ChangeMenu(BattleMenu.Selection);

                wasEnemyTurn = false;
            }
            if (Input.GetKeyDown(KeyCode.UpArrow))
            {
                if (currentSelection > 0)
                {
                    currentSelection--;
                }
            }
            if (Input.GetKeyDown(KeyCode.DownArrow))
            {
                if (currentSelection < 4)
                {
                    currentSelection++;
                }
            }
            if (currentSelection == 0)
            {
                currentSelection = 1;
            }

            // Making it possible to say what menu option player is choosing
            switch (currentMenu)
            {
                case BattleMenu.Selection:
                    switch (currentSelection)
                    {
                        case 1:
                            fightText.text = "> " + fightT;
                            bagText.text = bagT;
                            pokemonText.text = pokemonT;
                            runText.text = runT;
                            selectionInfoText.text = "Choose a move to attack.";
                            ChangeMenuIfButtonPressed(BattleMenu.Fight);
                            break;
                        case 2:
                            fightText.text = fightT;
                            bagText.text = "> " + bagT;
                            pokemonText.text = pokemonT;
                            runText.text = runT;
                            selectionInfoText.text = "Choose an item to use.";
                            break;
                        case 3:
                            fightText.text = fightT;
                            bagText.text = bagT;
                            pokemonText.text = "> " + pokemonT;
                            runText.text = runT;
                            selectionInfoText.text = "Choose another Pokemon.";
                            break;
                        case 4:
                            fightText.text = fightT;
                            bagText.text = bagT;
                            pokemonText.text = pokemonT;
                            runText.text = "> " + runT;
                            selectionInfoText.text = "Attempt to run away.";
                            ChangeMenuIfButtonPressed(BattleMenu.Info);
                            break;
                    }
                    break;
                case BattleMenu.Fight:
                    switch (currentSelection)
                    {
                        case 1:
                            moveO.text = "> " + moveOT;
                            moveT.text = moveTT;
                            moveTH.text = moveTHT;
                            moveF.text = moveFT;
                            DisplayMoveStatsOrChooseIt(0);
                            IfEscPressedReturnToSelection();
                            break;
                        case 2:
                            moveO.text = moveOT;
                            moveT.text = "> " + moveTT;
                            moveTH.text = moveTHT;
                            moveF.text = moveFT;
                            DisplayMoveStatsOrChooseIt(1);
                            IfEscPressedReturnToSelection();
                            break;
                        case 3:
                            moveO.text = moveOT;
                            moveT.text = moveTT;
                            moveTH.text = "> " + moveTHT;
                            moveF.text = moveFT;
                            DisplayMoveStatsOrChooseIt(2);
                            IfEscPressedReturnToSelection();
                            break;
                        case 4:
                            moveO.text = moveOT;
                            moveT.text = moveTT;
                            moveTH.text = moveTHT;
                            moveF.text = "> " + moveFT;
                            DisplayMoveStatsOrChooseIt(3);
                            IfEscPressedReturnToSelection();
                            break;
                    }
                    break;
                case BattleMenu.Info:
                    switch (previousMenu)
                    {
                        case BattleMenu.Selection:
                            //Debug.Log("A");
                            if (infoCounter == 1)
                            {
                                infoText.text = "Attempt to run away has failed!";
                                if (Input.GetKeyDown(KeyCode.Space))
                                {
                                    ChangeMenu(BattleMenu.Selection);
                                    infoCounter = 0;
                                    //Debug.Log("Space pressed!");
                                }
                            }
                            else
                            {
                                AttemptRunAway();
                                //Debug.Log("B");
                            }
                            break;
                        case BattleMenu.Fight:
                            
                            if(infoCounter == 0)
                            {
                                infoText.text = chosenPokemon.pName + " chose " + chosenPokemon.moves[chosenMove].Name + ".";
                                if (Input.GetKeyDown(KeyCode.Space))
                                {
                                    infoCounter = 1;
                                }
                            }
                            else
                            {
                                if (moveWasEffective == -1)
                                {
                                    infoText.text = "It had no effect.";
                                    if (Input.GetKeyDown(KeyCode.Space))
                                    {
                                        myTurn = false;
                                    }
                                }
                                if (moveWasEffective == 0)
                                {
                                    infoText.text = "It wasn't very effective.";
                                    if (Input.GetKeyDown(KeyCode.Space))
                                    {
                                        myTurn = false;
                                    }
                                }
                                if (moveWasEffective == 1)
                                {
                                    myTurn = false;
                                }
                                if (moveWasEffective == 2)
                                {
                                    infoText.text = "It was super effective!";
                                    if (Input.GetKeyDown(KeyCode.Space))
                                    {
                                        myTurn = false;
                                    }
                                }
                            }
                            break;
                        default:
                            //Debug.Log("Default");
                            break;
                    }
                    break;
            }
        }
        else
        {
            wasEnemyTurn = true;
            if(currentMenu == BattleMenu.Info && infoCounter == 0)
            {
                infoText.text = "Waiting for the enemy " + gameManager.battlePokemon.pName + " to make a move.";
            }
            else
            {
                ChangeMenu(BattleMenu.Info);
            }
        }
    }

    public void ChangeMenu(BattleMenu changeMenu)
    {
        if(currentMenu != BattleMenu.Info)
        {
            previousMenu = currentMenu;
        }
        //Debug.Log(currentMenu.ToString());
        currentMenu = changeMenu;
        currentSelection = 0;

        switch(changeMenu)
        {
            case BattleMenu.Selection:
                selectionInfo.gameObject.SetActive(true);
                selectionMenu.gameObject.SetActive(true);
                movesMenu.gameObject.SetActive(false);
                movesDetails.gameObject.SetActive(false);
                infoMenu.gameObject.SetActive(false);
                break;
            case BattleMenu.Fight:
                selectionInfo.gameObject.SetActive(false);
                selectionMenu.gameObject.SetActive(false);
                movesMenu.gameObject.SetActive(true);
                movesDetails.gameObject.SetActive(true);
                infoMenu.gameObject.SetActive(false);
                break;
            case BattleMenu.Info:
                selectionInfo.gameObject.SetActive(false);
                selectionMenu.gameObject.SetActive(false);
                movesMenu.gameObject.SetActive(false);
                movesDetails.gameObject.SetActive(false);
                infoMenu.gameObject.SetActive(true);
                break;
        }
    }

    public void ApplyDamageToEnemyPokemon(int moveIndex)
    {
        int ad;
        if(chosenPokemon.moves[moveIndex].category == MoveType.Physical)
        {
            ad = chosenPokemon.pokemonStats.AttackStat / gameManager.battlePokemon.pokemonStats.DefenceStat;
        }
        else
        {
            ad = chosenPokemon.pokemonStats.SpAttackStat / gameManager.battlePokemon.pokemonStats.SpDefenceStat;
        }

        // TODO: fix because the result doesn't match
        int damage = (int)math.round((((2 * chosenPokemon.level / 5 + 2) * chosenPokemon.moves[moveIndex].power * ad) / 50 + 2));

        PokemonType type = chosenPokemon.moves[moveIndex].moveType;
        if (gameManager.battlePokemon.damagedNormallyBy.Contains(type)) { }
        else
        {
            if (gameManager.battlePokemon.weakTo.Contains(type))
            {
                damage *= 2;
            }
            else
            {
                if (gameManager.battlePokemon.resistantTo.Contains(type))
                {
                    damage = (int)math.round(damage * 0.5);
                }
                else
                {
                    damage = 0;
                }
            }
        }
        Debug.Log("Damage dealt: " + damage.ToString());
        gameManager.battlePokemon.HP -= damage;

        if(gameManager.battlePokemon.HP <= 0)
        {
            gameManager.ExitBattle();
        }
    }

    private void ChangeMenuIfButtonPressed(BattleMenu changeMenu)
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            ChangeMenu(changeMenu);
        }
    }

    private void IfEscPressedReturnToSelection()
    {
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            ChangeMenu(BattleMenu.Selection);
        }
    }

    private void DisplayMoveStatsOrChooseIt(int selection)
    {
        pokemonType.text = "Typpe/" + chosenPokemon.moves[selection].moveType.ToString();
        PP.text = chosenPokemon.moves[selection].currentPP.ToString() +
            "/" + chosenPokemon.moves[selection].pp.ToString();
        
        if (Input.GetKeyDown(KeyCode.Space))
        {
            chosenPokemon.moves[selection].currentPP -= 1;
            chosenMove = selection;
            infoCounter = 0;

            // TODO: Switch the menu to Info
            ChangeMenu(BattleMenu.Info);

            // TODO: Calculate and apply damage to the enemy or changes to status
            if (chosenPokemon.moves[chosenMove].category != MoveType.Status)
            {
                ApplyDamageToEnemyPokemon(selection);
            }
        }
    }

    // returns true if successful
    private void AttemptRunAway()
    {
        int chance = UnityEngine.Random.Range(1, 100);
        Debug.Log(chance);
        if (chance > 50)
        {
            gameManager.ExitBattle();
            infoCounter = 0;
            ChangeMenu(BattleMenu.Selection);
        }
        else
        {
            infoCounter = 1;
        }
    }
}

public enum BattleMenu
{
    Selection,
    Pokemon,
    Bag,
    Fight,
    Info
}
