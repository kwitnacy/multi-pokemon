using System.Collections;
using System.Collections.Generic;
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
    }

    // Update is called once per frame
    void Update()
    {
        if(Input.GetKeyDown(KeyCode.UpArrow))
        {
            if(currentSelection > 0)
            {
                currentSelection--;
            }
        }
        if (Input.GetKeyDown(KeyCode.DownArrow))
        {
            if(currentSelection < 4)
            {
                currentSelection++;
            }
        }
        if(currentSelection == 0)
        {
            currentSelection = 1;
        }

        // Making it possible to say what menu option player is choosing
        switch(currentMenu)
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
                            if(Input.GetKeyDown(KeyCode.Space))
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
                    default:
                        //Debug.Log("Default");
                        break;
                }
                break;
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
            ChangeMenu(BattleMenu.Selection);
        }
    }

    // returns true if successful
    private void AttemptRunAway()
    {
        int chance = Random.Range(1, 100);
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
