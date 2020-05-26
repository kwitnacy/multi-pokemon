using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BattleManager : MonoBehaviour
{
    public BattleMenu currentMenu;

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

    // Start is called before the first frame update
    void Start()
    {
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
                        break;
                    case 2:
                        fightText.text = fightT;
                        bagText.text = "> " + bagT;
                        pokemonText.text = pokemonT;
                        runText.text = runT;
                        break;
                    case 3:
                        fightText.text = fightT;
                        bagText.text = bagT;
                        pokemonText.text = "> " + pokemonT;
                        runText.text = runT;
                        break;
                    case 4:
                        fightText.text = fightT;
                        bagText.text = bagT;
                        pokemonText.text = pokemonT;
                        runText.text = "> " + runT;
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
                        break;
                    case 2:
                        moveO.text = moveOT;
                        moveT.text = "> " + moveTT;
                        moveTH.text = moveTHT;
                        moveF.text = moveFT;
                        break;
                    case 3:
                        moveO.text = moveOT;
                        moveT.text = moveTT;
                        moveTH.text = "> " + moveTHT;
                        moveF.text = moveFT;
                        break;
                    case 4:
                        moveO.text = moveOT;
                        moveT.text = moveTT;
                        moveTH.text = moveTHT;
                        moveF.text = "> " + moveFT;
                        break;
                }
                break;
        }
    }

    public void ChangeMenu(BattleMenu changeMenu)
    {
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
}

public enum BattleMenu
{
    Selection,
    Pokemon,
    Bag,
    Fight,
    Info
}
